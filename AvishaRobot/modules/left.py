from AvishaRobot import pbot as app
from pyrogram import Client, filters, enums
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont

EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/avishaxbot?startgroup=true"),
    ],
]

# --------------------------------------------------------------------------------- #

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

# --------------------------------------------------------------------------------- #

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((286, 286))
        bg.paste(resized, (297, 117), resized)


    img_draw = ImageDraw.Draw(bg)

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path


# --------------------------------------------------------------------------------- #

bg_path = "AvishaRobot/Love/CUTELEF.jpg"
font_path = "AvishaRobot/Love/SwanseaBold-D0ox.ttf"

# --------------------------------------------------------------------------------- #

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {
            "banned", "left", "restricted"
        }
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = (
        member.old_chat_member.user
        if member.old_chat_member
        else member.from_user
    )

    # Check if the user has a profile photo
    if user.photo and user.photo.big_file_id:
        try:
            # Add the photo path, caption, and button details
            photo = await app.download_media(user.photo.big_file_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            caption = f"**ㅤㅤ  ㅤ◦•●◉✿ ᴜsᴇʀ ʟᴇғᴛ ✿◉●•◦\n▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰\n\n𖣐 ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ғʀᴏᴍ ɢʀᴏᴜᴘ.\n\n● ɢʀᴏᴜᴘ ➥ `{member.chat.title}`\n● ᴜsᴇʀ ɴᴀᴍᴇ ➥ {user.mention}\n● sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ, ʙᴀʙʏ.\n\n𖣐 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ [ʟ ᴜ ᴄ ʏ • / ‹𝟹](https://t.me/PhoenixXsupport)**\n▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰"

            # Send the message with the photo, caption, and button
            await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(EVAA),)
        except RPCError as e:
            print(e)
            return
    else:
        # Handle the case where the user has no profile photo
        print(f"𖣐 User {user.id} has no profile photo.")


# --------------------------------------------------------------------------------- #
# Goodbye Enable/Disable Command
@app.on_message(filters.command("zgoodbye", "/") & ~filters.private)
async def auto_state(_, message):
    usage = "**❅ ᴜsᴀɢᴇ ➥ **/zgoodbye [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ]"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        A = await wlcm.find_one({"chat_id": chat_id})
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "enable":
            if A:
                return await message.reply_text("๏ sᴘᴇᴄɪᴀʟ ɢᴏᴏᴅʙʏᴇ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ")
            else:
                await add_wlcm(chat_id)
                await message.reply_text(f"๏ ᴇɴᴀʙʟᴇᴅ sᴘᴇᴄɪᴀʟ ɢᴏᴏᴅʙʏᴇ ɪɴ ➥ {message.chat.title}")
        elif state == "disable":
            if not A:
                return await message.reply_text("๏ sᴘᴇᴄɪᴀʟ ɢᴏᴏᴅʙʏᴇ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ")
            else:
                await rm_wlcm(chat_id)
                await message.reply_text(f"๏ ᴅɪsᴀʙʟᴇᴅ sᴘᴇᴄɪᴀʟ ɢᴏᴏᴅʙʏᴇ ɪɴ ➥ {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("๏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ")