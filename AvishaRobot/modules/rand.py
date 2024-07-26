
from pyrogram import Client, filters
from faker import Faker
from AvishaRobot import pbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

fake = Faker()

EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/avishaxbot?startgroup=true"),
    ],
]

fake = Faker()

@app.on_message(filters.command("rand"))
def generate_info(client, message):
    # Generate fake data
    name = fake.name()
    address = fake.address()
    country = fake.country()
    phone_number = fake.phone_number()
    email = fake.email()
    city = fake.city()
    state = fake.state()
    zipcode = fake.zipcode()

    # Create a message with the fake data
    info_message = (
        f"𖣐 **ʀᴀɴᴅᴏᴍ ᴜsᴇʀ ᴀᴅᴅʀᴇss ᴅᴇᴛᴀɪʟs 𖣐**\n\n"
        
        f"**● ғᴜʟʟ ɴᴀᴍᴇ ➥** {name}\n"
        
        f"**● ᴀᴅᴅʀᴇss ➥** {address}\n"
        
        f"**● ᴄᴏᴜɴᴛʀʏ ➥** {country}\n"
        
        f"**● ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ➥** {phone_number}\n"
        
        f"**● ᴇᴍᴀɪʟ ➥** {email}\n"
        
        f"**● ᴄɪᴛʏ ➥** {city}\n"
        
        f"**● sᴛᴀᴛᴇ ➥** {state}\n"
        
        f"**● ᴢɪᴘᴄᴏᴅᴇ ➥** {zipcode}\n\n"

        f"𖣐 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ ʟ ᴜ ᴄ ʏ • / ‹𝟹"
    )
###
    
    message.reply_text(info_message, reply_markup=InlineKeyboardMarkup(EVAA),
    )

