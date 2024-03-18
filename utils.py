from datetime import datetime
from pytz import timezone
from config import Config
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def send_log(b, u):
    try:
        if Config.LOG_CHANNEL is not None:
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            Bot = await b.get_me()
            await b.send_message(
                Config.LOG_CHANNEL,
                f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.from_user.mention}\nIᴅ: `{u.from_user.id}`\nUɴ: @{u.from_user.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: {Bot.username}"
            )
    except Exception as e:
        print(e)

async def is_subscribed(bot, query):
    try:
        user = await bot.get_chat_member(Config.AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        logger.exception(e)
    else:
        if user.status != "banned":
            return True

    return False


async def force_sub(bot, cmd):
    invite_link = await bot.create_chat_invite_link(int(Config.AUTH_CHANNEL))
    buttons = [[InlineKeyboardButton(
        text="⚡ 𝖴𝗉𝖽𝖺𝗍𝖾𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 ⚡", url="invite_link.invite_link")]]
    text = "<blockquote>Please Join My Updates Channel to use this Bot!\n\nDue to Overload, Only Channel Subscribers can use this Bot!</blockquote>"

    return await cmd.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
