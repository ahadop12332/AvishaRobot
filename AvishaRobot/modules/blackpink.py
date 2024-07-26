from pyrogram import filters
from blackpink import blackpink as bp
from AvishaRobot import pbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/avishaxbot?startgroup=true"),
    ],
]

###
@app.on_message(filters.command("blackpink"))
async def blackpink(_, message):
    text = message.text[len("/blackpink ") :]
    bp(f"{text}").save(f"blackpink_{message.from_user.id}.png", caption=f"𖣐 ʙʟᴀᴄᴋᴘɪɴᴋ ʙʏ ➥ ʟ ᴜ ᴄ ʏ • / ‹𝟹", reply_markup=InlineKeyboardMarkup(EVAA),)
    await message.reply_photo(f"blackpink_{message.from_user.id}.png", caption=f"𖣐 ʙʟᴀᴄᴋᴘɪɴᴋ ʙʏ ➥ ʟ ᴜ ᴄ ʏ • / ‹𝟹", reply_markup=InlineKeyboardMarkup(EVAA),)
    os.remove(f"blackpink_{message.from_user.id}.png")
  
