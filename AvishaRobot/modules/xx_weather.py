from pyrogram import Client, filters
from AvishaRobot import pbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/nykaaxbot?startgroup=true"),
    ],
]

@app.on_message(filters.command("weather"))
def weather(client, message):
    try:
        # Get the location from user message
        user_input = message.command[1]
        location = user_input.strip()
        weather_url = f"https://wttr.in/{location}.png"
        
        # Reply with the weather information as a photo
        message.reply_photo(photo=weather_url, caption="𖣐 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ ʟ ᴜ ᴄ ʏ • / ‹𝟹", reply_markup=InlineKeyboardMarkup(EVAA),)
    except IndexError:
        # User didn't provide a location
        message.reply_text("⬤ Please provide a location. ♥︎ Use ➥ /weather NEW YORK")



__help__ = """

 ⬤ /weather <ᴄɪᴛʏ>* ➥* ᴀᴅᴠᴀɴᴄᴇᴅ ᴡᴇᴀᴛʜᴇʀ ᴍᴏᴅᴜʟᴇ, ᴜsᴀɢᴇ sᴀᴍᴇ ᴀs /ᴡᴇᴀᴛʜᴇʀ
 ⬤ /weather  ᴍᴏᴏɴ* ➥* ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs ᴏғ ᴍᴏᴏɴ
 ⬤ /calendar <year> ➥ sʜᴏᴡ ᴄᴀʟᴇɴᴅᴀʀ, ᴇx - 1984, 2004, 2024
 ⬤ /day ➥ sʜᴏᴡ ᴅᴀʏ, [● ᴇx ➣ 16/06/2003]
"""

__mod_name__ = "ᴡᴇᴀᴛʜᴇʀ"

