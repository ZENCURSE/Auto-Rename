"""Shared, defensive FFmpeg helpers used by the rename and media tools."""

import asyncio
import json
import os
import re
import shutil
from pathlib import Path

from config import Config


BRAND = "CodeRips"
MEDIA_EXTENSIONS = {
    ".3gp", ".avi", ".flac", ".m4a", ".m4v", ".mkv", ".mov", ".mp3",
    ".mp4", ".mpeg", ".mpg", ".ogg", ".opus", ".ts", ".wav", ".webm",
}
RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


class MediaCommandError(RuntimeError):
    """An FFmpeg/FFprobe command failed in a user-actionable way."""


def safe_filename(raw_name, extension, fallback="CodeRips_Renamed"):
    """Create a safe basename and apply exactly one output extension."""
    extension = re.sub(r"[^A-Za-z0-9.]", "", str(extension or ".mkv"))
    if not extension.startswith("."):
        extension = f".{extension}"
    if extension == ".":
        extension = ".mkv"

    name = os.path.basename(str(raw_name or "").strip())
    name = re.sub(r"[\x00-\x1f<>:\"/\\|?*]", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    while os.path.splitext(name)[1].lower() in MEDIA_EXTENSIONS:
        name = os.path.splitext(name)[0].strip(" .")

    if not name:
        name = fallback
    if name.upper() in RESERVED_NAMES:
        name = f"_{name}"

    # Leave room for the extension while respecting common filesystem limits.
    budget = max(1, 240 - len(extension.encode("utf-8")))
    name = name.encode("utf-8")[:budget].decode("utf-8", "ignore").rstrip(" .")
    return f"{name or fallback}{extension}"


async def _run_process(command, timeout, label):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except asyncio.TimeoutError as exc:
        process.kill()
        await process.wait()
        raise MediaCommandError(f"{label} timed out after {timeout} seconds") from exc

    error = stderr.decode(errors="replace").strip()
    if process.returncode != 0:
        detail = error[-900:] or f"exit code {process.returncode}"
        raise MediaCommandError(f"{label} failed: {detail}")
    return stdout, error


async def probe_media(path):
    """Return FFprobe JSON or raise a concise error."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise MediaCommandError("FFprobe is not installed on the server")
    if not os.path.isfile(path):
        raise MediaCommandError("The downloaded media file is missing")

    command = [
        ffprobe,
        "-v", "error",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        path,
    ]
    stdout, _ = await _run_process(
        command,
        max(10, int(getattr(Config, "FFPROBE_TIMEOUT", 120))),
        "FFprobe",
    )
    try:
        return json.loads(stdout.decode(errors="replace"))
    except json.JSONDecodeError as exc:
        raise MediaCommandError("FFprobe returned invalid media information") from exc


async def run_ffmpeg(command, output_path, label="FFmpeg"):
    """Run FFmpeg atomically so failed encodes never masquerade as valid files."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise MediaCommandError("FFmpeg is not installed on the server")
    if not command or command[0] != ffmpeg:
        raise ValueError("FFmpeg command must start with the discovered ffmpeg path")

    final_path = Path(output_path)
    partial_path = final_path.with_name(f".{final_path.name}.part")
    partial_path.unlink(missing_ok=True)
    command = [*command[:-1], str(partial_path)]
    try:
        await _run_process(
            command,
            max(30, int(getattr(Config, "FFMPEG_TIMEOUT", 1800))),
            label,
        )
        if not partial_path.is_file() or partial_path.stat().st_size == 0:
            raise MediaCommandError(f"{label} produced no output file")
        final_path.unlink(missing_ok=True)
        partial_path.replace(final_path)
        return str(final_path)
    finally:
        partial_path.unlink(missing_ok=True)


def _value(value, fallback=BRAND):
    value = str(value or "").strip()
    return value or fallback


async def metadata_values(database, user_id):
    """Read all metadata fields without making one missing field abort a job."""
    fields = ("title", "author", "artist", "audio", "subtitle", "video", "encoded_by", "custom_tag")
    values = await asyncio.gather(
        *(
            getattr(database, f"get_{field}")(user_id)
            for field in fields
        ),
        return_exceptions=True,
    )
    return {
        field: _value(value)
        for field, value in zip(fields, values)
        if not isinstance(value, Exception)
    } | {
        field: BRAND
        for field in fields
        if field not in {
            field_name for field_name, value in zip(fields, values)
            if not isinstance(value, Exception)
        }
    }


def metadata_args(values, streams=None):
    """Build portable FFmpeg metadata arguments and only tag existing streams."""
    args = []
    for field in ("title", "author", "artist", "encoded_by", "custom_tag"):
        args.extend(["-metadata", f"{field}={_value(values.get(field))}"])

    stream_tags = {
        "video": values.get("video"),
        "audio": values.get("audio"),
        "subtitle": values.get("subtitle"),
    }
    present = {stream.get("codec_type") for stream in (streams or [])}
    stream_prefix = {"video": "v", "audio": "a", "subtitle": "s"}
    for stream_type, value in stream_tags.items():
        if stream_type in present:
            args.extend([
                f"-metadata:s:{stream_prefix[stream_type]}",
                f"title={_value(value)}",
            ])
    return args