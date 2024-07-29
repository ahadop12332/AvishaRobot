import speedtest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from AvishaRobot import DEV_USERS, dispatcher
from AvishaRobot.modules.disable import DisableAbleCommandHandler
from AvishaRobot.modules.helper_funcs.chat_status import dev_plus


def convert(speed):
    return round(int(speed) / 1048576, 2)


@dev_plus
def speedtestxyz(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("ɪᴍᴀɢᴇ", callback_data="speedtest_image"),
            InlineKeyboardButton("ᴛᴇxᴛ", callback_data="speedtest_text"),
        ]
    ]

    update.effective_message.reply_text(
        "⬤ sᴩᴇᴇᴅᴛᴇsᴛ ᴍᴏᴅᴇ ⏤͟͟͞͞★", reply_markup=InlineKeyboardMarkup(buttons)
    )


def speedtestxyz_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.from_user.id in DEV_USERS:
        msg = update.effective_message.edit_text("⬤ ʀᴜɴɴɪɴɢ ᴀ sᴩᴇᴇᴅᴛᴇsᴛ...")
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = "⬤ sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛ ʙʏ ➥ ˹ ᴋᴧɪ ꭙ ꝛᴏʙσᴛ™ ♡゙"

        if query.data == "speedtest_image":
            speedtest_image = speed.results.share()
            update.effective_message.reply_photo(
                photo=speedtest_image, caption=replymsg
            )
            msg.delete()

        elif query.data == "speedtest_text":
            result = speed.results.dict()
            replymsg += f"\n\n⬤ ᴅᴏᴡɴʟᴏᴀᴅ ➥ `{convert(result['download'])} ᴍʙ/s`\n● ᴜᴘʟᴏᴀᴅ ➥ `{convert(result['upload'])}ᴍʙ/s`\n● ᴘɪɴɢ ➥ `{result['ping']}`\n\n𖣐 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ ˹ ᴋᴧɪ ꭙ ꝛᴏʙσᴛ™ ♡゙"
            update.effective_message.edit_text(replymsg, parse_mode=ParseMode.MARKDOWN)
    else:
        query.answer("⬤ ʏᴏᴜ ᴀʀᴇ ʀᴇǫᴜɪʀᴇᴅ ᴛᴏ ᴊᴏɪɴ @the_friendz ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")


SPEED_TEST_HANDLER = DisableAbleCommandHandler(
    "speedtest", speedtestxyz, run_async=True
)
SPEED_TEST_CALLBACKHANDLER = CallbackQueryHandler(
    speedtestxyz_callback, pattern="speedtest_.*", run_async=True
)

dispatcher.add_handler(SPEED_TEST_HANDLER)
dispatcher.add_handler(SPEED_TEST_CALLBACKHANDLER)

__help__ = """

⬤ /speedtest *➥* ʀᴜɴs ᴀ sᴘᴇᴇᴅᴛᴇsᴛ ᴀɴᴅ ᴄʜᴇᴄᴋ ᴛʜᴇ sᴇʀᴠᴇʀ sᴘᴇᴇᴅ.
"""

__mod_name__ = "s-ᴛᴇsᴛ"

__command_list__ = ["speedtest"]
__handlers__ = [SPEED_TEST_HANDLER, SPEED_TEST_CALLBACKHANDLER]
