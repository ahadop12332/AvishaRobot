from AvishaRobot import pbot as app
from pyrogram import filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from AvishaRobot.database.wel_db import wlcm
from PIL import Image, ImageDraw, ImageFont  # Ensure these are imported

EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url="https://t.me/avishaxbot?startgroup=true"),
    ],
]

# --------------------------------------------------------------------------------- #
# Helper Functions
get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: int,
    profile_path: str = None
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
# Goodbye message enable/disable command
@app.on_message(filters.command("zgoodbye", prefix='/') & ~filters.public)
async def auto_goodbye_state(_, message):
    usage = "**❅ Usage ➥ **/zgoodbye [enable|disable]"
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
            if A and A.get("goodbye_enabled", False):
                return await message.reply_text("๏ Special goodbye is already enabled.")
            else:
                await wlcm.update_one({"chat_id": chat_id}, {"$set": {"goodbye_enabled": True}}, upsert=True)
                await message.reply_text(f"๏ Enabled special goodbye in ➥ {message.chat.title}")
        elif state == "disable":
            if not A or not A.get("goodbye_enabled", False):
                return await message.reply_text("๏ Special goodbye is already disabled.")
            else:
                await wlcm.update_one({"chat_id": chat_id}, {"$set": {"goodbye_enabled": False}}, upsert=True)
                await message.reply_text(f"๏ Disabled special goodbye in ➥ {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("๏ Only admins can use this command")

# --------------------------------------------------------------------------------- #
# Goodbye message handler
@app.on_chat_member_updated(filters.group, group=-5)
async def member_has_left(client: app, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id": chat_id})

    # Check if goodbye is enabled
    if not A or not A.get("goodbye_enabled", False):
        return

    if (
        not member.new_chat_member
        and member.old_chat_member.status in {"banned", "left"}
    ):
        user = member.old_chat_member.user if member.old_chat_member else member.from_user

        # Check if the user has a profile photo
        if user.photo and user.photo.big_file_id:
            try:
                # Add the photo path, caption, and button details
                photo = await app.download_media(user.photo.big_file_id)

                goodbye_photo = await get_userinfo_img(
                    bg_path=bg_path,
                    font_path=font_path,
                    user_id=user.id,
                    profile_path=photo,
                )

                caption = f"**ㅤㅤ  ㅤ◦•●◉✿ ᴜsᴇʀ ʟᴇғᴛ ✿◉●•◦\n▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰\n\n𖣐 A member left from group.\n\n● Group ➥ `{member.chat.title}`\n● User name ➥ {user.mention}\n● See you soon again, baby.\n\n𖣐 Powered by ➥ [ʟ ᴜ ᴄ ʏ • / ‹𝟹](https://t.me/nova_xprobot)**\n▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰"

                # Send the message with the photo, caption, and button
                await client.send_photo(
                    chat_id=member.chat.id,
                    photo=goodbye_photo,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(EVAA),
                )
            except Exception as e:  # Catch general exceptions
                print(e)
                return
        else:
            # Handle the case where the user has no profile photo
            print(f"𖣐 User {user.id} has no profile photo.")