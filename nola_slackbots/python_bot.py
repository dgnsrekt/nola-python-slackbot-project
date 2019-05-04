from decouple import config
from .bot import bot_creater

TOKEN = config("PYTHON_BOT_USER_OAUTH_ACCESS_TOKEN")
BOT_CHANNEL_ID = config("PYTHON_BOT_CHANNEL")
BOT_DISPLAY_NAME = config("PYTHON_BOT_DISPLAY_NAME")
SYSTEM = "python"
TITLE_LINE_NUMBER = 1

python_rtm = bot_creater(
    token=TOKEN,
    bot_channel_id=BOT_CHANNEL_ID,
    bot_display_name=BOT_DISPLAY_NAME,
    system=SYSTEM,
    title_line_number=TITLE_LINE_NUMBER,
)
