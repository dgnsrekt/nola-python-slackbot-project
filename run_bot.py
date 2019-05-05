from decouple import config
from nola_slackbots.bot import bot_creater

TOKEN = config("OAUTH_ACCESS_TOKEN")
BOT_CHANNEL_ID = config("BOT_CHANNEL")
BOT_DISPLAY_NAME_ID = config("BOT_DISPLAY_NAME")
TOPIC = config("TOPIC")
TITLE_LINE_NUMBER = config("TITLE_LINE_NUMBER", cast=int)

rtm = bot_creater(
    token=TOKEN,
    bot_channel_id=BOT_CHANNEL_ID,
    bot_display_name_id=BOT_DISPLAY_NAME_ID,
    topic=TOPIC,
    title_line_number=TITLE_LINE_NUMBER,
)

if __name__ == "__main__":
    rtm.start()
