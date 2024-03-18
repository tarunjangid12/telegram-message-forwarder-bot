import os
from config import Config
import random
import logging
from time import sleep
import traceback
import asyncio
import sys

from pyrogram import filters

from bot import app, monitored_chats, chats_map, sudo_users
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from text import script
from database import userDb
from utils import is_subscribed, force_sub


logging.info("Bot Started")


@app.on_message(filters.chat(monitored_chats) & filters.incoming)
def work(_:Client, message:Message):
    caption = None
    msg = None
    chat = chats_map.get(message.chat.id)
    if chat.get("replace"):
        for old, new in chat["replace"].items():
            if message.media and not message.poll:
                caption = message.caption.markdown.replace(old, new)
            elif message.text:
                msg = message.text.markdown.replace(old, new)
    try:
        for chat in chat["to"]:
            if caption:
                message.copy(chat, caption=caption, parse_mode=ParseMode.MARKDOWN)
            elif msg:
                app.send_message(chat, msg, parse_mode=ParseMode.MARKDOWN)
            else:
                message.copy(chat)
    except Exception as e:
        logging.error(f"Error while sending message from {message.chat.id} to {chat}: {e}")


buttons=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Hᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="abt")
            ],
            [
                InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+mCdsJ7mjeBEyZWQ1"),
                InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/+HzGpLAZXTxoyYTNl")
            ]
        ]
        )


# Force Sub Handler
@Client.on_message(filters.private)
async def _(bot: Client, cmd):
    if not await is_subscribed(bot, cmd):
        return await force_sub(bot, cmd)

    await cmd.continue_propagation()


@Client.on_message(filters.private & filters.command('start'))
async def start(client, message:Message):


    await userDb.add_user(message.from_user.id, client, message)
    await client.send_message(
        chat_id=message.chat.id,
        text=script.START_MSG.format(
                message.from_user.first_name),
        reply_markup=buttons,
        parse_mode="html")


@Client.on_message(filters.command("stop"))
async def stop_button(bot, message):

    if str(message.from_user.id) not in Config.OWNER_ID:
        return
    msg = await bot.send_message(
        text="Stoping all processes...",
        chat_id=message.chat.id
    )
    await asyncio.sleep(1)
    await msg.edit("All Processes Stopped and Restarted")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.private & filters.command('help'))
async def help(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text=script.HELP_MSG,
        parse_mode="html")



@Client.on_callback_query(filters.regex(r'^back$'))
async def back_btn(bot,cb):
    await cb.message.edit_text(text=script.START_MSG.format(
                cb.from_user.first_name),
        reply_markup=buttons,
        parse_mode="html")

@Client.on_callback_query(filters.regex(r'^help$'))
async def cb_help(bot, cb):
    await cb.message.edit_text(script.HELP_MSG,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data='back')]]))



@Client.on_callback_query(filters.regex(r'^abt$'))   
async def cb_abt(bot, cb):
    await cb.message.edit_text(text=script.ABOUT_TXT, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data='back')]]))


@app.on_message(filters.user(sudo_users) & filters.command(["fwd", "forward"]), group=1)
def forward(client:Client, message:Message):
    if len(message.command) > 1 and message.command[1].isdigit():
        chat_id = int(message.command[1])
        if chat_id:
            try:
                offset_id = 0
                limit = 0
                if len(message.command) > 2:
                    limit = int(message.command[2])
                if len(message.command) > 3:
                    offset_id = int(message.command[3])
                for msg in client.get_chat_history(chat_id, limit=limit, offset_id=offset_id):
                    msg.copy(message.chat.id)
                    sleep(random.randint(1, 5))
            except Exception as e:
                message.reply_text(f"Error:\n```{traceback.format_exc()}```")
        else:
            message.reply_text(
                "Invalid Chat Identifier. Give me a chat id."
            )
    else:
        message.reply_text(
            "Invalid Command\nUse /fwd {chat_id} {limit} {first_message_id}"
        )


app.run()
