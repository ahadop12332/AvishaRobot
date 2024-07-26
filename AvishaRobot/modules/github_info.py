from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AvishaRobot import pbot
from AvishaRobot.utils.errors import capture_err


@pbot.on_message(filters.command(["github","git"]))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        return await message.reply_text("⬤ ᴇxᴀᴍᴘʟᴇ ➥ /github {username}")
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("⬤ ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʀɪɢʜᴛ ɢɪᴛʜᴜʙ ᴜsᴇʀɴᴀᴍᴇ.")
            result = await request.json()
            try:
                url = result["html_url"]
                name = result["name"]
                company = result["company"]
                bio = result["bio"]
                created_at = result["created_at"]
                avatar_url = result["avatar_url"]
                blog = result["blog"]
                location = result["location"]
                repositories = result["public_repos"]
                followers = result["followers"]
                following = result["following"]
                global Mukesh
                Mukesh = [[
            InlineKeyboardButton("ᴄʟᴏsᴇ",callback_data="close_reply")
            ]]     
                caption = f"""ㅤㅤ❖ ɢɪᴛʜᴜʙ ɪɴғᴏ ᴏғ {name} ⏤͟͟͞͞★
                 
● ᴜsᴇʀɴᴀᴍᴇ ➥ {username}
● ʙɪᴏ ➥ {bio}
● ʟɪɴᴋ ➥ [Here]({url})
● ᴄᴏᴍᴩᴀɴʏ ➥ {company}
● ᴄʀᴇᴀᴛᴇᴅ ᴏɴ ➥ {created_at}
● ʀᴇᴩᴏsɪᴛᴏʀɪᴇs ➥ {repositories}
● ʙʟᴏɢ ➥ {blog}
● ʟᴏᴄᴀᴛɪᴏɴ ➥ {location}
● ғᴏʟʟᴏᴡᴇʀs ➥ {followers}
● ғᴏʟʟᴏᴡɪɴɢ ➥ {following}

𖣐 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ [ʟ ᴜ ᴄ ʏ • / ‹𝟹](https://t.me/avishaxbot)"""
            except Exception as e:
                await message.reply(f"#ERROR {e}")
                  
    await message.reply_photo(photo=avatar_url, caption=caption,reply_markup=InlineKeyboardMarkup(Mukesh))


__mod_name__ = "ɢɪᴛʜᴜʙ"

__help__ = """

 ⬤ /github <ᴜsᴇʀɴᴀᴍᴇ> *➥* ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ɢɪᴛʜᴜʙ ᴜsᴇʀ.
"""

