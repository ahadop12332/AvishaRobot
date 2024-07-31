from pyrogram import Client, filters
from PIL import Image, ImageEnhance
from io import BytesIO
import aiohttp
import calendar
from AvishaRobot import pbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

EVAA = [
    [
        InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/PhoenixXsupport"),
    ],
]

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image_data = await resp.read()

    # Open the image using PIL
    carbon_image = Image.open(BytesIO(image_data))

    # Increase brightness
    enhancer = ImageEnhance.Brightness(carbon_image)
    bright_image = enhancer.enhance(1.7)  # Adjust the enhancement factor as needed

    # Save the modified image to BytesIO object with increased quality
    output_image = BytesIO()
    bright_image.save(output_image, format='PNG', quality=95)  # Adjust quality as needed
    output_image.name = "carbon.png"
    return output_image


@app.on_message(filters.command("calendar", prefixes="/"))
async def send_calendar(_, message):
    # Extract the year from the command arguments
    command_parts = message.text.split(" ")
    if len(command_parts) == 2:
        try:
            year = int(command_parts[1])
        except ValueError:
            await message.reply("⬤ ɪɴᴠᴀʟɪᴅ ʏᴇᴀʀ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ /calendar <year>")
            return
    else:
        await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ʏᴇᴀʀ ᴀғᴛᴇʀ ➥ /calendar ᴄᴏᴍᴍᴀɴᴅ.")
        return

    # Generate the calendar for the specified year
    cal = calendar.TextCalendar()
    full_year_calendar = cal.formatyear(year, 2, 1, 1, 3)

    # Generate the Carbon image for the calendar
    carbon_image = await make_carbon(full_year_calendar)

    # Send the image as a reply to the user
    await app.send_photo(message.chat.id, carbon_image, caption=f"𖣐 ʜᴇʀᴇ ɪs ʏᴏᴜʀ {year} ᴄᴀʟᴇɴᴅᴀʀ.", reply_markup=InlineKeyboardMarkup(EVAA),)

  
