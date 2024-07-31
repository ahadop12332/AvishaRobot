import os
import subprocess
import sys
from contextlib import suppress
from time import sleep

from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler

import AvishaRobot
from AvishaRobot import dispatcher
from AvishaRobot.modules.helper_funcs.chat_status import dev_plus


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.effective_message.reply_text(f"𖣐 ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴇ ᴏғ ᴀᴠɪsʜᴀ 𖣐 {AvishaRobot.ALLOW_CHATS}")
        return
    if args[0].lower() in ["off", "no"]:
        AvishaRobot.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        AvishaRobot.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("⬤ ғᴏʀᴍᴀᴛ ➥ /lockdown ʏᴇs/ɴᴏ ᴏʀ ᴏғғ/ᴏɴ")
        return
    update.effective_message.reply_text("⬤ ᴅᴏɴᴇ ! ʟᴏᴄᴋᴅᴏᴡɴ ᴠᴀʟᴜᴇ ᴛᴏɢɢʟᴇᴅ.")


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "⬤ ɪ ᴄᴏᴜʟᴅ ɴᴏᴛ ʟᴇᴀᴠᴇ ᴛʜᴀᴛ ɢʀᴏᴜᴘ(ᴅᴜɴɴᴏ ᴡʜʏ ᴛʜᴏ)."
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("⬤ ɪ ʟᴇғᴛ ᴛʜᴀᴛ sᴏᴜᴘ !.")
    else:
        update.effective_message.reply_text("⬤ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ")


@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "⬤ ᴘᴜʟʟɪɴɢ ᴀʟʟ ᴄʜᴀɴɢᴇs ғʀᴏᴍ ʀᴇᴍᴏᴛᴇ ᴀɴᴅ ᴛʜᴇɴ ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ."
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\n⬤ ᴄʜᴀɴɢᴇs ᴘᴜʟʟᴇᴅ...ɪ ɢᴜᴇss.. ʀᴇsᴛᴀʀᴛɪɴɢ ɪɴ "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("⬤ ʀᴇsᴛᴀʀᴛᴇᴅ.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "⬤ sᴛᴀʀᴛɪɴɢ ᴀ ɴᴇᴡ ɪɴsᴛᴀɴᴄᴇ ᴀɴᴅ sʜᴜᴛᴛɪɴɢ ᴅᴏᴡɴ ᴛʜɪs ᴏɴᴇ"
    )

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull, run_async=True)
RESTART_HANDLER = CommandHandler("reboot", restart, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "ᴏᴡɴᴇʀ"

__help__ = """

⬤ /leave ➥ ʟᴇᴀᴠᴇ ᴛʜᴇ ᴄʜᴀᴛ.
⬤ /gitpull ➥ ɢɪᴛғᴜʟʟ ᴛʜᴇ ʙᴏᴛ.
⬤ /reboot ➥ ʀᴇʙᴏᴏᴛ ᴛʜᴇ ʙᴏᴛ.
⬤ /lockdown ➥ ʟᴏᴄᴋᴅᴏᴡɴ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘs """

__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER, ALLOWGROUPS_HANDLER]
