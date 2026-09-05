"""Interactive media stream selection and remuxing.

This module intentionally stays separate from the legacy rename handler. It
owns only the short-lived per-user state needed between an inline button and
the final upload.
"""

import asyncio
import html
import logging
import os
import shutil
import tempfile
import uuid

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import Config
from helper.database import rexbots
from helper.utils import humanbytes, progress_for_pyrogram
from helper.media import (
    MediaCommandError,
    metadata_args,
    metadata_values,
    probe_media,
    run_ffmpeg,
    safe_filename,
)

logger = logging.getLogger(__name__)

MEDIA_STATE = {}
MEDIA_TIMEOUT = 30 * 60
MAX_MEDIA_SESSIONS = 256
MEDIA_ROOT = os.path.abspath(os.environ.get("MEDIA_JOB_DIR", os.path.join(tempfile.gettempdir(), "telegram-rename-media")))
def _button(text, data):
    return InlineKeyboardButton(text, callback_data=data)


def _callback(state, action, *parts):
    """Build callback data bound to the session that created the menu."""
    return ":".join(("media", state["nonce"], action, *map(str, parts)))


def _menu_keyboard(state):
    return InlineKeyboardMarkup([
        [_button("✏️ Rename File", _callback(state, "rename")),
         _button("ℹ️ Media Info", _callback(state, "info"))],
        [_button("🎵 Audio Tracks", _callback(state, "audio")),
         _button("📺 Subtitle Tracks", _callback(state, "subtitle"))],
        [_button("🎬 Video Tracks", _callback(state, "video")),
         _button("🗑 Remove Stream", _callback(state, "remove"))],
        [_button("⚙️ Encode + Rename", _callback(state, "encode"))],
        [_button("❌ Cancel", _callback(state, "cancel"))],
    ])


async def show_media_menu(message):
    user_id = message.from_user.id
    old = MEDIA_STATE.pop(user_id, None)
    if old:
        await _cleanup_state(old)
    # Keep state bounded even if users never press a button.
    await cleanup_expired_media_sessions()
    if len(MEDIA_STATE) >= MAX_MEDIA_SESSIONS:
        _, evicted = MEDIA_STATE.popitem()
        await _cleanup_state(evicted)
    state = {
        "source_message": message,
        "created_at": asyncio.get_running_loop().time(),
        "nonce": uuid.uuid4().hex[:16],
        "lock": asyncio.Lock(),
        "processing": False,
    }
    MEDIA_STATE[user_id] = state
    return await message.reply_text(
        "🎬 <b>Media actions</b>\n\n"
        "Choose an action. Stream buttons will be created from the actual "
        "audio, subtitle, and video tracks in your file.",
        reply_markup=_menu_keyboard(state),
    )


async def cleanup_expired_media_sessions():
    """Remove expired sessions and their private working directories."""
    now = asyncio.get_running_loop().time()
    expired = [
        (user_id, state) for user_id, state in MEDIA_STATE.items()
        if now - state["created_at"] > MEDIA_TIMEOUT
    ]
    for user_id, state in expired:
        if MEDIA_STATE.get(user_id) is state:
            MEDIA_STATE.pop(user_id, None)
            await _cleanup_state(state)


async def _state_for(query, nonce):
    state = MEDIA_STATE.get(query.from_user.id)
    if not state or state.get("nonce") != nonce:
        return None
    if asyncio.get_running_loop().time() - state["created_at"] > MEDIA_TIMEOUT:
        MEDIA_STATE.pop(query.from_user.id, None)
        await _cleanup_state(state)
        return None
    source = state.get("source_message")
    if not source or source.chat.id != query.message.chat.id:
        return None
    return state


async def _cleanup_state(state):
    job_dir = state.get("job_dir") if state else None
    if job_dir and os.path.isdir(job_dir):
        await asyncio.to_thread(shutil.rmtree, job_dir, True)


async def _fail(query, text):
    state = MEDIA_STATE.pop(query.from_user.id, None)
    await _cleanup_state(state)
    try:
        await query.message.edit_text(f"❌ {text}")
    except Exception:
        await query.message.reply_text(f"❌ {text}")


def _source_details(message):
    if message.document:
        media = message.document
        kind = "document"
    elif message.video:
        media = message.video
        kind = "video"
    else:
        return None
    return {
        "kind": kind,
        "file_name": media.file_name or f"media_{media.file_id[:8]}",
        "file_size": media.file_size or 0,
    }


async def _probe(path):
    return await probe_media(path)


async def _ensure_analyzed(client, query, state):
    if state.get("streams") is not None:
        return state

    details = _source_details(state["source_message"])
    if not details:
        raise RuntimeError("Only documents and videos support stream tools")
    if details["file_size"] > Config.MAX_FILE_SIZE:
        raise RuntimeError(
            f"File is {humanbytes(details['file_size'])}; the configured limit is "
            f"{humanbytes(Config.MAX_FILE_SIZE)}"
        )

    await query.message.edit_text("🔍 Analyzing media and detecting streams...")
    os.makedirs(MEDIA_ROOT, mode=0o700, exist_ok=True)
    job_dir = tempfile.mkdtemp(prefix=f"{query.from_user.id}-", dir=MEDIA_ROOT)
    os.chmod(job_dir, 0o700)
    extension = os.path.splitext(details["file_name"])[1].lower() or ".bin"
    source_path = os.path.join(job_dir, f"source{extension}")
    try:
        downloaded = await asyncio.wait_for(
            client.download_media(state["source_message"], file_name=source_path),
            timeout=MEDIA_TIMEOUT,
        )
        if not downloaded or not os.path.isfile(downloaded):
            raise FileNotFoundError("Telegram download completed without a local file")
        if os.path.getsize(downloaded) > Config.MAX_FILE_SIZE:
            raise RuntimeError("Downloaded file exceeds the configured size limit")
        info = await _probe(downloaded)
    except Exception:
        await asyncio.to_thread(shutil.rmtree, job_dir, True)
        raise

    streams = info.get("streams") or []
    if not streams:
        await asyncio.to_thread(shutil.rmtree, job_dir, True)
        raise MediaCommandError("FFprobe found no playable audio, video, or subtitle streams")
    state.update(
        job_dir=job_dir,
        source_path=downloaded,
        source_name=details["file_name"],
        source_kind=details["kind"],
        streams=streams,
        format_info=info.get("format") or {},
    )
    return state


def _language(stream):
    tags = stream.get("tags") or {}
    return tags.get("language") or tags.get("title") or "und"


def _stream_label(stream, ordinal=None):
    kind = stream.get("codec_type", "data")
    index = stream.get("index", "?")
    codec = (stream.get("codec_name") or "unknown").upper()
    language = _language(stream)
    tags = stream.get("tags") or {}
    title = tags.get("title")
    if kind == "audio":
        channels = stream.get("channels")
        detail = f"{channels}ch" if channels else "audio"
        return f"🎵 {language}" + (f" — {title}" if title else f" — {codec} — {detail}")
    if kind == "subtitle":
        return f"💬 {language}" + (f" — {title}" if title else f" — {codec}")
    if kind == "video":
        width, height = stream.get("width"), stream.get("height")
        size = f" — {width}x{height}" if width and height else ""
        return f"🎥 Video {ordinal or index} — {codec}{size}"
    return f"▪️ Stream {index} — {kind} — {codec}"


def _stream_list(state, kind=None):
    streams = state.get("streams") or []
    return [s for s in streams if kind is None or s.get("codec_type") == kind]


def _back_button(state):
    return [_button("‹ Back", _callback(state, "back"))]


async def _show_streams(query, state, kind, title, action):
    streams = _stream_list(state, kind)
    if not streams:
        await query.answer(f"No {kind or 'supported'} streams found", show_alert=True)
        return
    rows = []
    for stream in streams:
        rows.append([_button(
            _stream_label(stream),
            _callback(state, "pick", action, stream.get("index")),
        )])
    rows.append(_back_button(state))
    await query.message.edit_text(title, reply_markup=InlineKeyboardMarkup(rows))


def _info_text(state):
    lines = ["<b>ℹ️ Media information</b>"]
    for stream in state.get("streams") or []:
        tags = stream.get("tags") or {}
        details = [
            f"index {stream.get('index', '?')}",
            stream.get("codec_name") or "unknown codec",
        ]
        if stream.get("codec_type") == "audio":
            details.append(f"{stream.get('channels', '?')}ch")
        if stream.get("width") and stream.get("height"):
            details.append(f"{stream['width']}x{stream['height']}")
        if tags.get("language"):
            details.append(html.escape(str(tags["language"])))
        safe_details = [html.escape(str(detail)) for detail in details]
        lines.append(
            f"• <b>{html.escape(str(stream.get('codec_type', 'data')).title())}</b>: "
            + " — ".join(safe_details)
        )
    duration = (state.get("format_info") or {}).get("duration")
    if duration:
        lines.append(f"\nDuration: {duration}s")
    return "\n".join(lines)[:3900]


def _safe_output_name(raw, extension):
    return safe_filename(raw, extension, fallback="CodeRips_Renamed")


def _inside_job(job_dir, path):
    return os.path.commonpath((os.path.realpath(job_dir), os.path.realpath(path))) == os.path.realpath(job_dir)


async def _remux(state, action, stream_index):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise MediaCommandError("FFmpeg is not installed on the server")
    source_path = state["source_path"]
    # Matroska accepts arbitrary copied audio/subtitle/video layouts.
    extension = ".mkv"
    output_path = os.path.join(state["job_dir"], f"processed{extension}")

    if action == "remove":
        maps = ["-map", "0", "-map", f"-0:{stream_index}"]
    elif action == "audio":
        maps = ["-map", "0:v?", "-map", f"0:{stream_index}", "-map", "0:s?"]
    elif action == "subtitle":
        maps = ["-map", "0:v?", "-map", "0:a?", "-map", f"0:{stream_index}"]
    elif action == "video":
        maps = ["-map", f"0:{stream_index}", "-map", "0:a?", "-map", "0:s?"]
    else:
        raise RuntimeError("Unknown stream action")

    values = await metadata_values(rexbots, state["source_message"].from_user.id)
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-i", source_path,
        *maps,
        "-map_metadata", "0",
        "-c", "copy",
        *metadata_args(values, state.get("streams")),
        "-f", "matroska",
        "-y", output_path,
    ]
    try:
        await run_ffmpeg(command, output_path, label="FFmpeg remux")
    except Exception as first_error:
        # Attachments/data streams are not accepted by every Matroska build.
        # Retry with the normal media stream classes before showing an error.
        if action == "remove":
            fallback_maps = ["-map", "0:v?", "-map", "0:a?", "-map", "0:s?",
                             "-map", f"-0:{stream_index}"]
        elif action == "audio":
            fallback_maps = ["-map", "0:v?", "-map", f"0:{stream_index}", "-map", "0:s?"]
        elif action == "subtitle":
            fallback_maps = ["-map", "0:v?", "-map", "0:a?", "-map", f"0:{stream_index}"]
        else:
            fallback_maps = ["-map", f"0:{stream_index}", "-map", "0:a?", "-map", "0:s?"]
        fallback = [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-i", source_path,
            *fallback_maps, "-map_metadata", "0", "-c", "copy",
            *metadata_args(values, state.get("streams")),
            "-f", "matroska", "-y", output_path,
        ]
        try:
            await run_ffmpeg(fallback, output_path, label="FFmpeg remux")
        except Exception as second_error:
            raise MediaCommandError(f"Remux failed after fallback: {second_error}") from first_error
    await _probe(output_path)
    return output_path


async def _encode(state):
    """Encode to a compatible MKV while preserving all supported tracks."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise MediaCommandError("FFmpeg is not installed on the server")

    output_path = os.path.join(state["job_dir"], "encoded.mkv")
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-i", state["source_path"],
        "-map", "0:v:0?",
        "-map", "0:a?",
        "-map", "0:s?",
        "-map_metadata", "0",
        "-c:v", "libx264",
        "-preset", os.environ.get("ENCODE_PRESET", "veryfast"),
        "-crf", os.environ.get("ENCODE_CRF", "23"),
        "-c:a", "aac",
        "-b:a", os.environ.get("ENCODE_AUDIO_BITRATE", "192k"),
        "-c:s", "copy",
        *metadata_args(
            await metadata_values(rexbots, state["source_message"].from_user.id),
            state.get("streams"),
        ),
        "-f", "matroska",
        "-y", output_path,
    ]
    await run_ffmpeg(command, output_path, label="FFmpeg encode")
    await _probe(output_path)
    return output_path


async def _ask_and_upload(client, query, state, processed_path):
    extension = os.path.splitext(processed_path)[1].lower() or ".mkv"
    await query.message.edit_text(
        "📁 <b>Send the new filename</b>\n\n"
        f"The extension will stay {extension}.\nSend /cancel to stop."
    )
    try:
        reply = await client.listen(
            chat_id=query.message.chat.id,
            filters=filters.text,
            timeout=300,
        )
    except asyncio.TimeoutError:
        raise RuntimeError("Filename request timed out")
    raw_name = (reply.text or "").strip()
    if raw_name.lower() == "/cancel":
        raise RuntimeError("Operation cancelled")
    output_name = _safe_output_name(raw_name, extension)
    final_path = os.path.join(state["job_dir"], output_name)
    if not _inside_job(state["job_dir"], final_path):
        raise RuntimeError("Invalid output filename")
    os.replace(processed_path, final_path)

    caption_template = await rexbots.get_caption(query.from_user.id)
    caption = output_name
    if caption_template:
        try:
            caption = caption_template.format(
                filename=output_name,
                filesize=humanbytes(os.path.getsize(final_path)),
                duration=(state.get("format_info") or {}).get("duration", "N/A"),
            )
        except (KeyError, ValueError):
            logger.warning("Invalid caption template for user %s", query.from_user.id)
    caption = caption[:1024]
    status = await query.message.edit_text("📤 Uploading processed file...")
    upload_args = {
        "chat_id": query.message.chat.id,
        "caption": caption,
        "parse_mode": None,
        "progress": progress_for_pyrogram,
        "progress_args": ("📤 Uploading...", status, asyncio.get_running_loop().time()),
    }
    if extension in {".mp4", ".m4v", ".webm"} and any(
        s.get("codec_type") == "video" for s in state.get("streams", [])
    ):
        await client.send_video(video=final_path, **upload_args)
    else:
        await client.send_document(document=final_path, **upload_args)
    return output_name


async def handle_media_callback(client, query):
    data = query.data or ""
    await query.answer()
    parts = data.split(":")
    if len(parts) < 3 or parts[0] != "media":
        return
    nonce, action, args = parts[1], parts[2], parts[3:]
    state = await _state_for(query, nonce)
    if action == "cancel":
        if state and MEDIA_STATE.get(query.from_user.id) is state:
            MEDIA_STATE.pop(query.from_user.id, None)
            await _cleanup_state(state)
        return await query.message.edit_text("❌ Media operation cancelled.")
    if not state:
        return await query.message.edit_text("⚠️ This media session expired. Please send the file again.")

    try:
        async with state["lock"]:
            if state["processing"]:
                return await query.message.edit_text("⚙️ This media operation is already processing.")
            return await _handle_media_action(client, query, state, action, args)
    except Exception as exc:
        logger.exception("Media operation failed for user %s", query.from_user.id)
        detail = html.escape(str(exc).strip()[:500] or "unknown error")
        await _fail(query, f"Media operation failed:\n<code>{detail}</code>")


async def _handle_media_action(client, query, state, action, args):
        if action == "rename":
            MEDIA_STATE.pop(query.from_user.id, None)
            await _cleanup_state(state)
            await query.message.edit_text("✏️ Starting the normal rename flow...")
            from plugins.file_rename import auto_rename_files
            return await auto_rename_files(client, state["source_message"], force=True)

        await _ensure_analyzed(client, query, state)
        if action == "back":
            return await query.message.edit_text(
                "🎬 <b>Media actions</b>\nChoose an action:",
                reply_markup=_menu_keyboard(state),
            )
        if action == "info":
            return await query.message.edit_text(_info_text(state), reply_markup=InlineKeyboardMarkup(_back_button(state)))
        if action == "audio":
            return await _show_streams(query, state, "audio", "🎵 <b>Audio Tracks</b>", "audio")
        if action == "subtitle":
            return await _show_streams(query, state, "subtitle", "📺 <b>Subtitle Tracks</b>", "subtitle")
        if action == "video":
            return await _show_streams(query, state, "video", "🎬 <b>Video Tracks</b>", "video")
        if action == "remove":
            return await _show_streams(query, state, None, "🗑 <b>Remove Stream</b>", "remove")
        if action == "pick" and len(args) == 2:
            picked_action, index = args
            if picked_action not in {"audio", "subtitle", "video", "remove"}:
                raise RuntimeError("Invalid stream action")
            stream = next((s for s in state["streams"] if str(s.get("index")) == index), None)
            if not stream:
                return await query.message.edit_text("⚠️ That stream is no longer available.")
            state["pending_action"] = picked_action
            state["pending_index"] = int(index)
            label = _stream_label(stream)
            if picked_action == "remove":
                text = f"🗑 Remove <b>{label}</b>?\nThis cannot be undone for this output."
            else:
                text = f"✅ Keep only <b>{label}</b> for this stream type?"
            return await query.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup([
                    [_button("✅ Confirm", _callback(state, "confirm")), _button("❌ Cancel", _callback(state, "back"))]
                ]),
            )
        if action == "confirm":
            action = state.pop("pending_action", None)
            index = state.pop("pending_index", None)
            if action is None or index is None:
                return await query.message.edit_text("⚠️ No stream selection is pending.", reply_markup=_menu_keyboard(state))
            state["processing"] = True
            await query.message.edit_text("⚙️ Processing with stream-copy remux...")
            processed = await _remux(state, action, index)
            name = await _ask_and_upload(client, query, state, processed)
            MEDIA_STATE.pop(query.from_user.id, None)
            await _cleanup_state(state)
            return await query.message.edit_text(f"✅ Completed: <code>{name}</code>")
        if action == "encode":
            state["processing"] = True
            await query.message.edit_text(
                "⚙️ Encoding media with H.264/AAC and applying CodeRips metadata..."
            )
            processed = await _encode(state)
            name = await _ask_and_upload(client, query, state, processed)
            MEDIA_STATE.pop(query.from_user.id, None)
            await _cleanup_state(state)
            return await query.message.edit_text(f"✅ Encode completed: <code>{name}</code>")
        return await query.message.edit_text("⚠️ Unknown media action.", reply_markup=_menu_keyboard(state))