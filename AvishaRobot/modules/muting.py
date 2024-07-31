import html
from typing import Optional

from telegram import Bot, Chat, ChatPermissions, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

from AvishaRobot import LOGGER, TIGERS, dispatcher
from AvishaRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    user_admin,
)
from AvishaRobot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from AvishaRobot.modules.helper_funcs.string_handling import extract_time
from AvishaRobot.modules.log_channel import loggable


def check_user(user_id: int, bot: Bot, chat: Chat) -> Optional[str]:
    if not user_id:
        reply = "𖣐 You don't seem to be referring to a user or the ID specified is incorrect.."
        return reply

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "𖣐 User not found":
            reply = "𖣐 I can't seem to find this user"
            return reply
        else:
            raise

    if user_id == bot.id:
        reply = "𖣐 I'm not gonna MUTE myself, How high are you?"
        return reply

    if is_user_admin(chat, user_id, member) or user_id in TIGERS:
        reply = "𖣐 Can't. Find someone else to mute but not this one."
        return reply

    return None


@connection_status
@bot_admin
@user_admin
@loggable
def mute(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#MUTE\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    if member.can_send_messages is None or member.can_send_messages:
        chat_permissions = ChatPermissions(can_send_messages=False)
        bot.restrict_chat_member(chat.id, user_id, chat_permissions)
        bot.sendMessage(
            chat.id,
            f"𖣐 ᴍᴜᴛᴇᴅ <b>{html.escape(member.user.first_name)}</b> ᴡɪᴛʜ ɴᴏ ᴇxᴘɪʀᴀᴛɪᴏɴ ᴅᴀᴛᴇ.",
            parse_mode=ParseMode.HTML,
        )
        return log

    else:
        message.reply_text("𖣐 ᴛʜɪs ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ.")

    return ""
@connection_status
@bot_admin
@user_admin
@loggable
def dmute(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    
    user_id, reason = extract_user_and_text(message, args)
    bot.delete_message(chat, message_id)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#MUTE\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    if member.can_send_messages is None or member.can_send_messages:
        chat_permissions = ChatPermissions(can_send_messages=False)
        bot.restrict_chat_member(chat.id, user_id, chat_permissions)

        return log

    else:
        pass
    return ""
    

@connection_status
@bot_admin
@user_admin
@loggable
def unmute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "𖣐 You'll need to either give me a username to unmute, or reply to someone to be unmuted."
        )
        return ""

    member = chat.get_member(int(user_id))

    if member.status != "kicked" and member.status != "left":
        if (
            member.can_send_messages
            and member.can_send_media_messages
            and member.can_send_other_messages
            and member.can_add_web_page_previews
        ):
            message.reply_text("𖣐 ᴛʜɪs ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ʜᴀs ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ sᴘᴇᴀᴋ.")
        else:
            chat_permissions = ChatPermissions(
                can_send_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_send_polls=True,
                can_change_info=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            )
            try:
                bot.restrict_chat_member(chat.id, int(user_id), chat_permissions)
            except BadRequest:
                pass
            bot.sendMessage(
                chat.id,
                f"𖣐 ɪ sʜᴀʟʟ ᴀʟʟᴏᴡ <b>{html.escape(member.user.first_name)}</b> ᴛᴏ ᴛᴇxᴛ.",
                parse_mode=ParseMode.HTML,
            )
            return (
                f"❖ <b>ᴜsᴇʀ ᴜɴᴍᴜᴛᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ {html.escape(chat.title)} ⏤͟͟͞͞★</b>\n\n"
                f"● <b>ᴀᴅᴍɪɴ ➥ </b> {mention_html(user.id, user.first_name)}\n"
                f"● <b>ᴜsᴇʀ ➥ </b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        message.reply_text(
            "𖣐 This user isn't even in the chat, unmuting them won't make them talk more than they "
            "already do!"
        )

    return ""


@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    if not reason:
        message.reply_text("𖣐 You haven't specified a time to mute this user for!")
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#TEMP MUTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    try:
        if member.can_send_messages is None or member.can_send_messages:
            chat_permissions = ChatPermissions(can_send_messages=False)
            bot.restrict_chat_member(
                chat.id, user_id, chat_permissions, until_date=mutetime
            )
            bot.sendMessage(
                chat.id,
                f"⬤ ᴍᴜᴛᴇᴅ <b>{html.escape(member.user.first_name)}</b> ғᴏʀ {time_val}!",
                parse_mode=ParseMode.HTML,
            )
            return log
        else:
            message.reply_text("𖣐 ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ.")

    except BadRequest as excp:
        if excp.message == "𖣐 Reply message not found":
            # Do not reply
            message.reply_text(f"⬤ ᴍᴜᴛᴇᴅ ғᴏʀ {time_val}!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "⬤ ERROR muting user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("𖣐 ɪ ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ ᴛʜᴀᴛ ᴜsᴇʀ.")

    return ""

__help__ = """

 ⬤ /mute  <ᴜsᴇʀʜᴀɴᴅʟᴇ>* ➥* ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ.
 ⬤ /tmute  <ᴜsᴇʀʜᴀɴᴅʟᴇ> x(ᴍ/ʜ/ᴅ)* ➥* ᴍᴜᴛᴇs ᴀ ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). `ᴍ` = `ᴍɪɴᴜᴛᴇs`, `ʜ` = `ʜᴏᴜʀs`, `ᴅ` = `ᴅᴀʏs`.
 ⬤ /unmute <ᴜsᴇʀʜᴀɴᴅʟᴇ>* ➥* ᴜɴᴍᴜᴛᴇs ᴀ ᴜsᴇʀ.
 ⬤ /dmute <ᴜsᴇʀʜᴀɴᴅʟᴇ>* ➥* ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ.
"""
DMUTE_HANDLER = CommandHandler("dmute", dmute, run_async=True)
MUTE_HANDLER = CommandHandler("mute", mute, run_async=True)
UNMUTE_HANDLER = CommandHandler("unmute", unmute, run_async=True)
TEMPMUTE_HANDLER = CommandHandler(["tmute", "tempmute"], temp_mute, run_async=True)
dispatcher.add_handler(DMUTE_HANDLER)
dispatcher.add_handler(MUTE_HANDLER)
dispatcher.add_handler(UNMUTE_HANDLER)
dispatcher.add_handler(TEMPMUTE_HANDLER)

__mod_name__ = "ᴍᴜᴛᴇ"

__handlers__ = [DMUTE_HANDLER,MUTE_HANDLER, UNMUTE_HANDLER, TEMPMUTE_HANDLER]
