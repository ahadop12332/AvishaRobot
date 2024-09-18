import os  # Environment variables ke liye os module import karna

class Config(object):
    LOGGER = True

    #####

    ANILIST_CLIENT = os.getenv("ANILIST_CLIENT", "8679")
    ANILIST_SECRET = os.getenv("ANILIST_SECRET", "NeCEq9A1hVnjsjZlTZyNvqK11krQ4HtSliaM7rTN")
    API_ID = os.getenv("API_ID", None)
    API_HASH = os.getenv("API_HASH", None)
    TOKEN = os.getenv("TOKEN", None)
    OWNER_ID = os.getenv("OWNER_ID", "7202110938")
    OWNER_USERNAME = ("OWNER_USERNAME", "itslucciii")
    SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "PhoenixXsupport")
    START_IMG = os.getenv("START_IMG", "https://graph.org/file/eaa3a2602e43844a488a5.jpg")
    JOIN_LOGGER = os.getenv("JOIN_LOGGER", "-1002059639505")
    EVENT_LOGS = os.getenv("EVENT_LOGS", "-1002059639505")
    ERROR_LOGS = os.getenv("ERROR_LOGS", "-1002059639505")
    MONGO_DB_URI = os.getenv("MONGO_DB_URI", None)
    LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1002059929123")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "nova_xprobot")
    DATABASE_URL = os.getenv("DATABASE_URL", None)
    CASH_API_KEY = os.getenv("CASH_API_KEY", "V48U2FLLKRHSVD4X")
    TIME_API_KEY = os.getenv("TIME_API_KEY", "1CUBX1HXGNHW")
    SPAMWATCH_API = os.getenv("SPAMWATCH_API", "3624487efd8e4ca9c949f1ab99654ad1e4de854f41a14afd00f3ca82d808dc8c")
    SPAMWATCH_SUPPORT_CHAT = os.getenv("SPAMWATCH_SUPPORT_CHAT", "h_cc_help")
    WALL_API = os.getenv("WALL_API", "2455acab48f3a935a8e703e54e26d121")
    REM_BG_API_KEY = os.getenv("REM_BG_API_KEY", "xYCR1ZyK3ZsofjH7Y6hPcyzC")
    OPENWEATHERMAP_ID = os.getenv("OPENWEATHERMAP_ID", "887da2c60d9f13fe78b0f9d0c5cbaade")
    BAN_STICKER = os.getenv("BAN_STICKER", "CAACAgEAAxkBAAIrTWYljyX_lqcubkAzg0jy45CRvxAFAAKvAgACrLHoRU50VVvh3xWwNAQ")
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", None)
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", None)
    LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "8f3315b5806c21004b2822f07825187d")

    # OpenAI API key ko environment se fetch karna
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please add your OpenAI API key in the environment variables.")

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True