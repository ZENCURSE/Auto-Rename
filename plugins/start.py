# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
import requests
import random
import asyncio
import base64
import logging
import string
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatAction, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from datetime import datetime, timedelta
from functools import wraps
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
from helper.database import *
from config import Config
from .callbacks import cb_handler
from plugins.helper_func import *
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
chat_data_cache = {}
ADMIN_URL = Config.ADMIN_URL
FSUB_PIC = Config.FSUB_PIC
BOT_USERNAME = Config.BOT_USERNAME
OWNER_ID = Config.OWNER_ID
FSUB_LINK_EXPIRY = 10
active_tasks = {}
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def check_ban(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        user = await rexbots.col.find_one({"_id": user_id})
        if user and user.get("ban_status", {}).get("is_banned", False):
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ...!!", url=ADMIN_URL)]]
            )
            return await message.reply_text(
                "Wᴛғ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ʙʏ ᴏᴜʀ ᴀᴅᴍɪɴ/ᴏᴡɴᴇʀ . Iғ ʏᴏᴜ ᴛʜɪɴᴋs ɪᴛ's ᴍɪsᴛᴀᴋᴇ ᴄʟɪᴄᴋ ᴏɴ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ...!!",
                reply_markup=keyboard
            )
        return await func(client, message, *args, **kwargs)
    return wrapper
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def check_user_premium(user_id):
    """Check if user has premium access - handles missing method gracefully"""
    try:
        # First check if the method exists
        if hasattr(rexbots, 'has_premium_access'):
            return await rexbots.has_premium_access(user_id)
        else:
            # Fallback: Check database directly
            user_data = await rexbots.col.find_one({"_id": user_id})
            if not user_data:
                return False
            
            # Check for premium in user data
            premium_data = user_data.get("premium", {})
            
            # Check if premium is active and not expired
            is_premium = premium_data.get("is_premium", False)
            expiry_date = premium_data.get("expiry_date")
            
            if is_premium and expiry_date:
                if isinstance(expiry_date, datetime):
                    return expiry_date > datetime.utcnow()
                else:
                    return True
            
            return is_premium
    except Exception as e:
        logger.error(f"Error checking premium status: {e}")
        return False
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def check_verification(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        logger.debug(f"check_verification decorator called for user {user_id}")
        
        try:
            text = message.text
            if len(text) > 7:
                try:
                    param = text.split(" ", 1)[1]
                    if param.startswith("verify_"):
                        token = param[7:]
                        await handle_verification_callback(client, message, token)
                        return
                        
                except Exception as e:
                    logger.error(f"Error processing start parameter: {e}")
    
            # Step 1: Check if user has premium access - premium users bypass verification
            try:
                if await check_user_premium(user_id):
                    logger.debug(f"User {user_id} has premium, bypassing verification")
                    return await func(client, message, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error checking premium status in decorator: {e}")
                # Continue with verification check even if premium check fails
            
            # Step 2: Get verification settings to check if verification is enabled
            settings = await rexbots.get_verification_settings()
            verify_status_1 = settings.get("verify_status_1", False)
            verify_status_2 = settings.get("verify_status_2", False)
            
            # If both verification systems are disabled, allow access
            if not verify_status_1 and not verify_status_2:
                logger.debug(f"Verification disabled, allowing user {user_id}")
                return await func(client, message, *args, **kwargs)
            
            # Step 3: Check if user is already verified (EXACTLY like /verify command)
            try:
                if await is_user_verified(user_id):
                    try:
                        user_data = await rexbots.col.find_one({"_id": user_id}) or {}
                        verification_data = user_data.get("verification", {})
                        
                        verified_time_1 = verification_data.get("verified_time_1")
                        verified_time_2 = verification_data.get("verified_time_2")
                        
                        current_time = datetime.utcnow()
                        
                        # Check if fully verified (shortener 1 within 24 hours)
                        if verified_time_1:
                            try:
                                if isinstance(verified_time_1, datetime) and current_time < verified_time_1 + timedelta(hours=24):
                                    time_left = timedelta(hours=24) - (current_time - verified_time_1)
                                    hours_left = time_left.seconds // 3600
                                    minutes_left = (time_left.seconds % 3600) // 60
                                    
                                    await show_start_message(client, message)
                                    return 
                            except Exception as e:
                                logger.error(f"Error checking verified_time_1: {e}")

                        # Check if fully verified (shortener 2 within 24 hours)
                        if verified_time_2:
                            try:
                                if isinstance(verified_time_2, datetime) and current_time < verified_time_2 + timedelta(hours=24):
                                    time_left = timedelta(hours=24) - (current_time - verified_time_2)
                                    hours_left = time_left.seconds // 3600
                                    minutes_left = (time_left.seconds % 3600) // 60
                                    
                                    await show_start_message(client, message)
                                    return 
                            except Exception as e:
                                logger.error(f"Error checking verified_time_2: {e}")
                                
                    except Exception as e:
                        logger.error(f"Error checking verification status: {e}")
            except Exception as e:
                logger.error(f"Error in is_user_verified check: {e}")

            
            # Step 4: User is NOT verified - send verification message
            logger.debug(f"User {user_id} is not verified, sending verification prompt")

            try:
                await send_verification_message(client, message)
            except Exception as e:
                logger.error(f"Error sending verification message in decorator: {e}")
                await message.reply_text(
                    f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ZENCURSE</i></b>\n"
                    f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {str(e)}</blockquote>"
                )
            return
            
        except Exception as e:
            logger.error(f"FATAL ERROR in check_verification decorator: {e}")
            await message.reply_text(
                f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ZENCURSE</i></b>\n"
                f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {str(e)}</blockquote>"
            )
            return
    
    return wrapper
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------        
async def check_admin(filter, client, update):
    try:
        user_id = update.from_user.id
        return any([user_id == OWNER_ID, await rexbots.admin_exist(user_id)])
    except Exception as e:
        logger.error(f"Exception in check_admin: {e}")
        return False
            
admin = filters.create(check_admin)
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def check_fsub(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        logger.debug(f"check_fsub decorator called for user {user_id}")

        async def is_sub(client, user_id, channel_id):
            try:
                member = await client.get_chat_member(channel_id, user_id)
                return member.status in {
                    ChatMemberStatus.OWNER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.MEMBER
                }
            except UserNotParticipant:
                mode = await rexbots.get_channel_mode(channel_id)
                if mode == "on":
                    exists = await rexbots.req_user_exist(channel_id, user_id)
                    return exists
                return False
            except Exception as e:
                logger.error(f"Error in is_sub(): {e}")
                return False

        async def is_subscribed(client, user_id):
            channel_ids = await rexbots.show_channels()
            if not channel_ids:
                return True
            if user_id == OWNER_ID:
                return True
            for cid in channel_ids:
                if not await is_sub(client, user_id, cid):
                    mode = await rexbots.get_channel_mode(cid)
                    if mode == "on":
                        await asyncio.sleep(2)
                        if await is_sub(client, user_id, cid):
                            continue
                    return False
            return True
        
        try:
            is_sub_status = await is_subscribed(client, user_id)
            logger.debug(f"User {user_id} subscribed status: {is_sub_status}")
            
            if not is_sub_status:
                logger.debug(f"User {user_id} is not subscribed, calling not_joined.")
                return await not_joined(client, message)
            
            logger.debug(f"User {user_id} is subscribed, proceeding with function call.")
            return await func(client, message, *args, **kwargs)
        
        except Exception as e:
            logger.error(f"FATAL ERROR in check_fsub: {e}")
            await message.reply_text(f"An unexpected error occurred: {e}. Please contact the developer.")
            return
    return wrapper
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def not_joined(client: Client, message: Message):
    logger.debug(f"not_joined function called for user {message.from_user.id}")
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>")

    # Add a check to ensure temp message exists before proceeding
    if not temp:
        logger.warning("Failed to send temporary message in not_joined")
        return

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await rexbots.show_channels()
        for chat_id in all_channels:
            await message.reply_chat_action(ChatAction.TYPING)

            is_member = False
            try:
                member = await client.get_chat_member(chat_id, user_id)
                is_member = member.status in {
                    ChatMemberStatus.OWNER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.MEMBER
                }
            except UserNotParticipant:
                is_member = False
            except Exception as e:
                is_member = False
                logger.error(f"Error checking member in not_joined: {e}")

            if not is_member:
                try:
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title
                    mode = await rexbots.get_channel_mode(chat_id)

                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                        )
                        link = invite.invite_link
                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    try:
                        await temp.edit(f"<b>{'! ' * count}</b>")
                    except Exception as e:
                        logger.warning(f"Failed to edit message in not_joined: {e}")


                except Exception as e:
                    logger.error(f"Error with chat {chat_id}: {e}")
                    await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ZENCURSE</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )
                    return

        try:
            buttons.append([
                InlineKeyboardButton(
                    text='• Jᴏɪɴᴇᴅ •',
                    url=f"https://t.me/{Config.BOT_USERNAME}?start=true"
                )
            ])
        except IndexError:
            pass

        text = "<b>Yᴏᴜ Bᴀᴋᴋᴀᴀ...!! \n\n<blockquote>Jᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍʏ ᴏᴛʜᴇʀᴡɪsᴇ Yᴏᴜ ᴀʀᴇ ɪɴ ʙɪɢ sʜɪᴛ...!!</blockquote></b>"
        if temp:
            try:
                await temp.delete()
            except Exception as e:
                logger.warning(f"Failed to delete temp message in not_joined: {e}")
        
        logger.debug(f"Sending final reply photo to user {user_id}")
        await message.reply_photo(
            photo=FSUB_PIC,
            caption=text,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        logger.error(f"Final Error in not_joined: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ZENCURSE</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command("start"))
@check_ban
@check_verification
@check_fsub
async def start(client, message: Message):
    logger.debug(f"/start command received from user {message.from_user.id}")
    user_id = message.from_user.id
    
    text = message.text
    
    # Check if there's a parameter after /start
    if len(text) > 7:
        try:
            param = text.split(" ", 1)[1]
            
            # Check if it's a verification callback
            if param.startswith("verify_"):
                token = param[7:]
                await handle_verification_callback(client, message, token)
                return
                
        except Exception as e:
            logger.error(f"Error processing start parameter: {e}")
    
    # Normal start command - show welcome message
    await rexbots.add_user(client, message)
    await show_start_message(client, message)

async def show_start_message(client, message: Message):
    """Show the start message with buttons"""
    m = await message.reply_text("Wᴇᴡ...Hᴏᴡ ᴀʀᴇ ʏᴏᴜ ᴅᴜᴅᴇ \nᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ. . .")
    await asyncio.sleep(0.2)
    await m.edit_text("🎊")
    await asyncio.sleep(0.2)
    await m.edit_text("⚡")
    await asyncio.sleep(0.2)
    await message.reply_chat_action(ChatAction.CHOOSE_STICKER)
    await asyncio.sleep(3)
    await m.edit_text("Iᴀᴍ sᴛᴀʀᴛɪɴɢ...!!")
    await asyncio.sleep(0.4)
    await m.delete()

    await message.reply_sticker("CAACAgUAAxkBAAEOcZBoHtzt2LPLp2H6yTblKDPdT9oroQACrRUAAmSm2FeGMk8-cGYtcDYE")

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴds •", callback_data='help')
        ],
        [
            InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url='https://t.me/CodeRips'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/Code_Rips_Support')
        ],
        [
            InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('Dᴇᴠᴇʟᴏᴘᴇʀ•', url='https://t.me/ZENCURSE')
        ]
    ])

    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Config.START_TXT.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=Config.START_TXT.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=buttons,
            disable_web_page_preview=True
        )
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def handle_verification_callback(client, message: Message, token: str):
    """Handle when user returns after completing verification through shortlink"""
    user_id = message.from_user.id
    current_time = datetime.utcnow()
    
    logger.info(f"[VERIFY] Starting verification callback for user {user_id} with token {token}")
    
    try:
        # Get verification settings
        settings = await rexbots.get_verification_settings()
        verify_status_1 = settings.get("verify_status_1", False)
        verify_status_2 = settings.get("verify_status_2", False)
        
        logger.info(f"[VERIFY] Settings - verify_status_1: {verify_status_1}, verify_status_2: {verify_status_2}")
        
        # If verification is disabled, just show start message
        if not verify_status_1 and not verify_status_2:
            logger.info(f"[VERIFY] Verification disabled, showing start message")
            await show_start_message(client, message)
            return 
        
        # Find the user who owns this token
        logger.info(f"[VERIFY] Looking up token in database for user {user_id}")
        token_owner = await rexbots.col.find_one({
            "_id": user_id,
            "verification.pending_token": token
        })
        
        if not token_owner:
            logger.warning(f"[VERIFY] Token not found in database!")
            await message.reply_text(
                "❌ Iɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ ᴛᴏᴋᴇɴ!\n\n"
                "Pʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ ʙʏ ᴜsɪɴɢ /verify"
            )
            return
        
        logger.info(f"[VERIFY] Token found! Extracting verification data...")
        verification_data = token_owner.get("verification", {})
        token_user_id = verification_data.get("token_user_id")
        token_created_at = verification_data.get("token_created_at")
        
        logger.info(f"[VERIFY] token_user_id: {token_user_id}, token_created_at: {token_created_at}")
        selected_shortener = verification_data.get("selected_shortener")
        
        # Check if token belongs to this user
        if token_user_id != user_id:
            logger.warning(f"[VERIFY] Token mismatch! Expected {user_id}, got {token_user_id}")
            await message.reply_text(
                "❌ Tʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ!\n\n"
                "Pʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ʟɪɴᴋ ᴜsɪɴɢ /verify"
            )
            return
        
        # Check if token has expired (24 hours)
        if token_created_at:
            time_diff = current_time - token_created_at
            logger.info(f"[VERIFY] Time difference: {time_diff.total_seconds()} seconds")
            
            if time_diff > timedelta(hours=24):
                logger.warning(f"[VERIFY] Token expired!")
                await message.reply_text(
                    "❌ Yᴏᴜʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛᴏᴋᴇɴ ʜᴀs ᴇxᴘɪʀᴇᴅ!\n\n"
                    "Pʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ʟɪɴᴋ ᴜsɪɴɢ /verify"
                )
                # Clear expired token
                await rexbots.col.update_one(
                    {"_id": user_id},
                    {"$unset": {
                        "verification.pending_token": "",
                        "verification.token_created_at": "",
                        "verification.token_user_id": ""
                    }}
                )
                return
            
            # Check for bypass (verification completed too quickly
            if time_diff < timedelta(minutes=1):
                logger.warning(f"[VERIFY] Bypass detected! Completed in {time_diff.total_seconds()} seconds")
                await message.reply_text(
                    f"⚠️ Bʏᴘᴀss Dᴇᴛᴇᴄᴛᴇᴅ!\n\n"
                    f"• Yᴏᴜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛᴏᴏ ǫᴜɪᴄᴋʟʏ ({int(time_diff.total_seconds())} sᴇᴄᴏɴᴅs).\n\n"
                    f"Pʟᴇᴀsᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ᴛʜᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴘᴇʀʟʏ. Usᴇ /verify ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ʟɪɴᴋ."
                )
                # Clear the token
                await rexbots.col.update_one(
                    {"_id": user_id},
                    {"$unset": {
                        "verification.pending_token": "",
                        "verification.token_created_at": "",
                        "verification.token_user_id": ""
                    }}
                )
                return
        
        # All checks passed - Update verification time (24 hour validity)
        logger.info(f"[VERIFY] All checks passed! Updating database...")
        
        update_result = await rexbots.col.update_one(
            {"_id": user_id},
            {"$set": {
                "verification.verified_time_1": current_time,
                "verification.verified_time_2": current_time
            },
             "$unset": {
                "verification.pending_token": "",
                "verification.token_created_at": "",
                "verification.token_user_id": ""
             }},
            upsert=True
        )
        
        logger.info(f"[VERIFY] Database update result: matched={update_result.matched_count}, modified={update_result.modified_count}")
        
        # Calculate time taken
        time_taken = current_time - token_created_at if token_created_at else timedelta(0)
        minutes_taken = int(time_taken.total_seconds() // 60)
        seconds_taken = int(time_taken.total_seconds() % 60)
        
        logger.info(f"[VERIFY] Sending success message to user {user_id}")
        
        # Send success message
        await message.reply_text(
            f"✅ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!\n\n"
            f"›› ʏᴏᴜʀ ᴛᴏᴋᴇɴ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ ᴀɴᴅ ɪs ᴠᴀʟɪᴅ ғᴏʀ 24ʜᴏᴜʀs ‼️\n\n"
            f"⏱️ Tɪᴍᴇ ᴛᴀᴋᴇɴ: {minutes_taken}m {seconds_taken}s\n\n"
            f"Nᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("•Sᴇᴇ ᴘʟᴀɴs •", callback_data="seeplan")
            ]])
        )
        
        logger.info(f"[VERIFY] Verification complete for user {user_id}!")
        if selected_shortener:
            await rexbots.save_verification(user_id, selected_shortener)
        
    except Exception as e:
        logger.error(f"[VERIFY] FATAL ERROR in handle_verification_callback: {e}", exc_info=True)
        await message.reply_text(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ZENCURSE</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {str(e)}</blockquote>"
        )
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------        
async def send_verification_message(client, message: Message):
    """Generate and send verification shortlink to user"""
    user_id = message.from_user.id

    # Check if user has premium
    if await check_user_premium(user_id):
        await message.reply_text(
            "✨ <b>Yᴏᴜ ʜᴀᴠᴇ Pʀᴇᴍɪᴜᴍ Aᴄᴄᴇss!</b>\n\n"
            "Pʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴅᴏɴ'ᴛ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("•Sᴇᴇ ᴘʟᴀɴs •", callback_data="seeplan")
            ]])
        )
        return

    # Get verification settings
    settings = await rexbots.get_verification_settings()
    verify_status_1 = settings.get("verify_status_1", False)
    verify_status_2 = settings.get("verify_status_2", False)
    verified_time_1 = settings.get("verified_time_1")
    verified_time_2 = settings.get("verified_time_2")
    
    # Get available shorteners
    available_shorteners = []
    if verify_status_1:
        available_shorteners.append(1)
    if verify_status_2:
        available_shorteners.append(2)
    
    if not available_shorteners:
        await show_start_message(client, message)
        return 
    
    # Randomly select a shortener from available ones
    selected_shortener = random.choice(available_shorteners)
    
    # Generate a random token for verification
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Store token with user_id and creation time (for expiry and ownership check)
    current_time = datetime.utcnow()
    await rexbots.col.update_one(
        {"_id": user_id},
        {"$set": {
            "verification.pending_token": token,
            "verification.token_created_at": current_time,
            "verification.token_user_id": user_id,
            "verification.selected_shortener": selected_shortener
        }},
        upsert=True
    )
    
    # This is the bot deep link that shortener will redirect to
    redirect_url = f"https://t.me/{Config.BOT_USERNAME}?start=verify_{token}"
    
    # Get shortlink from the shortener API
    shortlink = await get_shortlink(redirect_url, selected_shortener)
    
    if not shortlink:
        await message.reply_text(
            "Eʀʀᴏʀ ɢᴇɴᴇʀᴀᴛɪɴɢ sʜᴏʀᴛʟɪɴᴋ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ @ZENCURSE."
        )
        return None
    
    # Send button with shortlink (e.g., https://lksfy.com/eARog)
    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton("• Vᴇʀɪғʏ •", url=shortlink)
    ]])
    
    await message.reply_text(
        f"ʜᴇʏ {message.from_user.mention},\n\n"
        "‼️ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴅᴀʏ ‼️\n\n"
        "⚠️ Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴀᴄᴄᴇss ᴏғ ʀᴇɴᴀᴍɪɴɢ ᴛʜᴇ ғɪʟᴇs\n\n"
        "Cʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ.\n\n"
        "⏰ <b>Vᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴠᴀʟɪᴅ ғᴏʀ 24 ʜᴏᴜʀs</b>\n"
        "<b>Tᴏᴋᴇɴ ᴇxᴘɪʀᴇs ɪɴ 24 ʜᴏᴜʀs</b>",
        reply_markup=buttons
    )
    
    return shortlink
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.command("cancel"))
async def cancel_handler(client, message):
    user_id = message.from_user.id
    
    if user_id in active_tasks:
        task = active_tasks.pop(user_id)
        task.cancel()
        await message.reply_text("Pʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ...!!")
    else:
        await message.reply_text("Nᴏ ᴀᴄᴛɪᴠᴇ ᴘʀᴏᴄᴇss ᴛᴏ ᴄᴀɴᴄᴇʟ...!!")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.command("verify_settings") & admin)
async def verify_settings(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴠᴇʀɪꜰʏ 𝟷", callback_data="verify_1_cbb"), InlineKeyboardButton("ᴠᴇʀɪꜰʏ 𝟸", callback_data="verify_2_cbb")],
        [InlineKeyboardButton("ᴄᴏᴜɴᴛs", callback_data="verify_count")]
    ])
    await message.reply_text(
        "ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇꜱꜱ:\n\n ➲ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ᴛᴜʀɴ ᴏɴ/ᴏꜰꜰ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇꜱꜱ & Aʟsᴏ ʏᴏᴜ ᴄᴀɴ sᴇᴇ ᴄᴏᴜɴᴛs.",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

async def get_shortlink(link, shortener_num):
    """Generate a shortlink using the specified shortener (1 or 2)
    
    Args:
        link: The redirect URL (e.g., https://t.me/Bot?start=verify_token)
        shortener_num: Which shortener to use (1 or 2)
    
    Returns:
        Shortened URL (e.g., https://lksfy.com/eARog)
    """
    settings = await rexbots.get_verification_settings()
    
    if shortener_num == 1:
        api = settings.get("verify_token_1", "Not set")
        site = settings.get("api_link_1", "Not set")
    else:
        api = settings.get("verify_token_2", "Not set")
        site = settings.get("api_link_2", "Not set")
    
    if site == "Not set" or api == "Not set":
        logger.error(f"Shortener {shortener_num} settings missing: {site} or {api}")
        return None
    
    try:
        resp = requests.get(f"https://{site}/api?api={api}&url={link}").json()
        if resp.get('status') == 'success' and 'shortenedUrl' in resp:
            return resp['shortenedUrl']
        else:
            logger.error(f"Shortlink API error: {resp}")
            return None
    except Exception as e:
        logger.error(f"Error generating shortlink: {e}")
        try:
            resp = requests.get(f"https://{site}/api?api={api}&url={link}").json()
            return resp.get('shortenedUrl') if resp.get('status') == 'success' else None
        except Exception as e2:
            logger.error(f"Fallback shortlink failed: {e2}")
            return None
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def is_user_verified(user_id):
    """Check if user is verified (either verified_time_1 or verified_time_2 is valid)"""
    try:
        user_data = await rexbots.col.find_one({"_id": user_id})
        if not user_data:
            return False
        
        verification_data = user_data.get("verification", {})
        verified_time_1 = verification_data.get("verified_time_1")
        verified_time_2 = verification_data.get("verified_time_2")
        
        current_time = datetime.utcnow()
        
        # Check if either verification is valid (within 24 hours)
        if verified_time_1:
            if isinstance(verified_time_1, datetime):
                if current_time < verified_time_1 + timedelta(hours=24):
                    return True
        
        if verified_time_2:
            if isinstance(verified_time_2, datetime):
                if current_time < verified_time_2 + timedelta(hours=24):
                    return True
        
        return False
    except Exception as e:
        logger.error(f"Error checking if user is verified: {e}")
        return False
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.command("verify") & filters.private)
async def verify_command(client, message: Message):
    """Check verification status or initiate verification"""
    user_id = message.from_user.id
    
    try:
        # Check if user has premium
        if await check_user_premium(user_id):
            await message.reply_text(
                "✨ <b>Yᴏᴜ ʜᴀᴠᴇ Pʀᴇᴍɪᴜᴍ Aᴄᴄᴇss!</b>\n\n"
                "Pʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴅᴏɴ'ᴛ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("•Sᴇᴇ ᴘʟᴀɴs •", callback_data="seeplan")
                ]])
            )
            return
    except Exception as e:
        logger.error(f"Error checking premium status in verify command: {e}")
        # Continue with verification check even if premium check fails

    try:
        # Check if user is already verified
        if await is_user_verified(user_id):
            try:
                user_data = await rexbots.col.find_one({"_id": user_id}) or {}
                verification_data = user_data.get("verification", {})
                
                # Get verification settings
                settings = await rexbots.get_verification_settings()
                verified_time_1 = verification_data.get("verified_time_1")
                verified_time_2 = verification_data.get("verified_time_2")
                
                current_time = datetime.utcnow()
                
                # Check if fully verified (shortener 1 within 24 hours)
                if verified_time_1:
                    try:
                        if isinstance(verified_time_1, datetime) and current_time < verified_time_1 + timedelta(hours=24):
                            time_left = timedelta(hours=24) - (current_time - verified_time_1)
                            hours_left = time_left.seconds // 3600
                            minutes_left = (time_left.seconds % 3600) // 60
                            
                            await message.reply_text(
                                f"✅ Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴠᴇʀɪғɪᴇᴅ!\n\n"
                                f"⏰ Tɪᴍᴇ ʟᴇғᴛ: {hours_left}ʜ {minutes_left}ᴍ",
                                reply_markup=InlineKeyboardMarkup([[
                                    InlineKeyboardButton("•Sᴇᴇ ᴘʟᴀɴs •", callback_data="seeplan")
                                ]])
                            )
                            return
                    except Exception as e:
                        logger.error(f"Error checking verified_time_1: {e}")

                # Check if fully verified (shortener 2 within 24 hours)
                if verified_time_2:
                    try:
                        if isinstance(verified_time_2, datetime) and current_time < verified_time_2 + timedelta(hours=24):
                            time_left = timedelta(hours=24) - (current_time - verified_time_2)
                            hours_left = time_left.seconds // 3600
                            minutes_left = (time_left.seconds % 3600) // 60
                            
                            await message.reply_text(
                                f"✅ Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴠᴇʀɪғɪᴇᴅ!\n\n"
                                f"⏰ Tɪᴍᴇ ʟᴇғᴛ: {hours_left}ʜ {minutes_left}ᴍ",
                                reply_markup=InlineKeyboardMarkup([[
                                    InlineKeyboardButton("•Sᴇᴇ ᴘʟᴀɴs •", callback_data="seeplan")
                                ]])
                            )
                            return
                    except Exception as e:
                        logger.error(f"Error checking verified_time_2: {e}")
                        
            except Exception as e:
                logger.error(f"Error checking verification status: {e}")
                # Continue to generate new verification link if there's an error
    
    except Exception as e:
        logger.error(f"Error in is_user_verified check: {e}")
    
    # User not verified - generate and send verification link
    try:
        await send_verification_message(client, message)
    except Exception as e:
        logger.error(f"Error sending verification message: {e}")
        await message.reply_text(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @ZENCURSE</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {str(e)}</blockquote>"
        )



# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
