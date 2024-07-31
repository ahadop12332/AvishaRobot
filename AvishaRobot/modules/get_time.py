import datetime
from typing import List

import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from AvishaRobot import TIME_API_KEY, dispatcher
from AvishaRobot.modules.disable import DisableAbleCommandHandler


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"https://api.timezonedb.com/v2.1/list-time-zone"
        f"?key={TIME_API_KEY}"
        f"&format=json"
        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst"
    ).json()

    for zone in data["zones"]:
        for eachtype in findtype:
            if to_find in zone[eachtype].lower():
                country_name = zone["countryName"]
                country_zone = zone["zoneName"]
                country_code = zone["countryCode"]

                if zone["dst"] == 1:
                    daylight_saving = "Yes"
                else:
                    daylight_saving = "No"

                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone["gmtOffset"]
                timestamp = datetime.datetime.now(
                    datetime.timezone.utc
                ) + datetime.timedelta(seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)

                break

    try:
        result = (
            f"𖣐 ᴄᴜʀʀʀɴᴛ ᴛɪᴍᴇ ᴏғ {country_name} ⏤͟͟͞͞★\n\n"
            f"● <b>ᴄᴏᴜɴᴛʀʏ ➥</b> <code>{country_name}</code>\n"
            f"● <b>ᴢᴏɴᴇ ɴᴀᴍᴇ ➥</b> <code>{country_zone}</code>\n"
            f"● <b>ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ ➥</b> <code>{country_code}</code>\n"
            f"● <b>ᴅᴀʏʟɪɢʜᴛ sᴀᴠɪɴɢ ➥</b> <code>{daylight_saving}</code>\n"
            f"● <b>ᴅᴀʏ ➥</b> <code>{current_day}</code>\n"
            f"● <b>ᴄᴜʀʀᴇɴᴛ ᴛɪᴍᴇ ➥</b> <code>{current_time}</code>\n"
            f"● <b>ᴄᴜʀʀᴇɴᴛ ᴅᴀᴛᴇ ➥</b> <code>{current_date}</code>\n"
            '● <b>ᴛɪᴍᴇᴢᴏɴᴇs ➥</b> <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones">ʟɪsᴛ ʜᴇʀᴇ</a>'
        )
    except:
        result = None

    return result


def gettime(update: Update, context: CallbackContext):
    message = update.effective_message

    try:
        query = message.text.strip().split(" ", 1)[1]
    except:
        message.reply_text("⬤ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄᴏᴜɴᴛʀʏ ɴᴀᴍᴇ/ᴀʙʙʀᴇᴠɪᴀᴛɪᴏɴ/ᴛɪᴍᴇᴢᴏɴᴇ ᴛᴏ ғɪɴᴅ.")
        return
    send_message = message.reply_text(
        f"⬤ ғɪɴᴅɪɴɢ ᴛɪᴍᴇᴢᴏɴᴇ ɪɴғᴏ ғᴏʀ <b>{query}</b>", parse_mode=ParseMode.HTML
    )

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        send_message.edit_text(
            f"⬤ ᴛɪᴍᴇᴢᴏɴᴇ ɪɴғᴏ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ <b>{query}</b>\n"
            '<b>ᴀʟʟ ᴛɪᴍᴇᴢᴏɴᴇs ➥</b> <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones">ʟɪsᴛ ʜᴇʀᴇ</a>',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        return

    send_message.edit_text(
        result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )


__help__ = """

 ⬤ /time <ǫᴜᴇʀʏ> ➥ ɢɪᴠᴇs ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴛɪᴍᴇᴢᴏɴᴇ.
"""

TIME_HANDLER = DisableAbleCommandHandler("time", gettime, run_async=True)

dispatcher.add_handler(TIME_HANDLER)

__mod_name__ = "ᴛɪᴍᴇ"

__command_list__ = ["time"]
__handlers__ = [TIME_HANDLER]
  
