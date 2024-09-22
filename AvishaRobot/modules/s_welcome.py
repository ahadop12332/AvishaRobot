import os
import random
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger

from AvishaRobot import pbot as app
from AvishaRobot.database.wel_db import *

COMMAND_HANDLER = [".", "/"]  # Command handlers

LOGGER = getLogger(__name__)

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname):
    background = Image.open("AvishaRobot/resources/bg.jpg")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((450, 450)) 
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('AvishaRobot/resources/SwanseaBold-D0ox.ttf', size=44)
    welcome_font = ImageFont.truetype('AvishaRobot/resources/SwanseaBold-D0ox.ttf', size=90)
    draw.text((65, 250), f'NAME : {unidecode(user)}', fill=(255, 255, 255), font=font)
    draw.text((65, 340), f'ID : {id}', fill=(255, 255, 255), font=font)
    draw.text((65, 430), f"USERNAME : {uname}", fill=(255,255,255), font=font)
    pfp_position = (767, 133)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

@app.on_message(filters.command("zwelcome", COMMAND_HANDLER) & filters.group)
async def auto_state(_, message):
    usage = "**❅ ᴜsᴀɢᴇ ➥ **/zwelcome [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ]"
    
    if len(message.command) == 1:
        return await message.reply_text(usage)
    
    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)
    
    # Check if the user is an admin or owner
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply("๏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ")
    
    # Fetch welcome state from the database
    A = await wlcm.find_one({"chat_id": chat_id})
    state = message.text.split(None, 1)[1].strip().lower()

    # Enable special welcome
    if state == "enable":
        if A:
            return await message.reply_text("๏ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ")
        await add_wlcm(chat_id)  # Add welcome settings to the database
        return await message.reply_text(f"๏ ᴇɴᴀʙʟᴇᴅ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ɪɴ ➥ {message.chat.title}")
    
    # Disable special welcome
    elif state == "disable":
        if not A:
            return await message.reply_text("๏ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ")
        await rm_wlcm(chat_id)  # Remove welcome settings from the database
        return await message.reply_text(f"๏ ᴅɪsᴀʙʟᴇᴅ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ɪɴ ➥ {message.chat.title}")
    
    # Invalid state
    else:
        return await message.reply_text(usage)


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    
    # Check if special welcome is enabled
    A = await wlcm.find_one({"chat_id": chat_id})
    
    # If no entry is found (meaning welcome is disabled), exit the function
    if not A:
        return
    
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"restricted"}
        or member.old_chat_member
    ):
        return
    
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "HuTao/resources/profilepic.jpg"
    
    if temp.MELCOW.get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption= f"""
**ㅤㅤㅤ◦•●◉✿ ᴡᴇʟᴄᴏᴍᴇ ʙᴀʙʏ ✿◉●•◦
▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰

● ɢʀᴏᴜᴘ ➥ {member.chat.title}
● ɴᴀᴍᴇ ➥ {user.mention}
● ᴜsᴇʀ ɪᴅ ➥ {user.id}
● ᴜsᴇʀɴᴀᴍᴇ ➥ @{user.username}

𖣐 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ [ʟ ᴜ ᴄ ʏ • / ‹𝟹゙](https://t.me/where_lucy)**
▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰
""",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"ᴠɪᴇᴡ ᴜsᴇʀ", url=f"https://t.me/{user.username}")]])
        )
    except Exception as e:
        LOGGER.error(e)
    
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        return