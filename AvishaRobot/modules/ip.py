from pyrogram import Client, filters

import requests

from AvishaRobot import pbot as app


@app.on_message(filters.command(["ipinfo"]))
def ip_info(_, message):
    if len(message.command) != 2:
        message.reply_text("⬤ Please provide an IP address after the command. Example: /ipinfo 8.8.8.8")
        return

    ip_address = message.command[1]
    info = get_ip_info(ip_address)

    if info:
        message.reply_text(info)
    else:
        message.reply_text("⬤ Unable to fetch information for the provided IP address.")


def get_ip_info(ip_address):
    api_url = f"https://api.safone.dev/ipinfo?ip={ip_address}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            info = f"𖣐 ɪᴘ ➥ {data['ip']}\n● ᴄᴏᴜɴᴛʀʏ ➥ {data['country']}\n● ᴄɪᴛʏ ➥ {data['city']}\n𖣐 ɪsᴘ ➥ {data['isp']}"
            return info
    except Exception as e:
        print(f"⬤ Error fetching IP information ➥ {e}")

  
