from decouple import config
import slack
from time import time

TOKEN = config("PYTHON_BOT_USER_OAUTH_ACCESS_TOKEN")
BOT_CHANNEL_ID = config("PYTHON_BOT_CHANNEL")

# TOKEN = config("GIT_BOT_USER_OAUTH_ACCESS_TOKEN")
# BOT_CHANNEL_ID = config("GIT_BOT_CHANNEL")

TOKEN = config("BASH_BOT_USER_OAUTH_ACCESS_TOKEN")
BOT_CHANNEL_ID = config("BASH_BOT_CHANNEL")


def prepare_message(title, message):
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"{title}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"```{message}```"}},
    ]


def payload_parser(payload):
    data = payload.get("data")
    web_client = payload.get("web_client")
    rtm_client = payload.get("rtm_client")

    channel = data.get("channel")
    user = data.get("user")
    text = data.get("text")

    return web_client, rtm_client, channel, user, text


@slack.RTMClient.run_on(event="message")
def ping(**payload):
    start = time()

    web_client, rtm_client, channel, user, text = payload_parser(payload)
    print(text)
    if user:
        if "ping" in text:

            web_client.chat_postMessage(channel=channel, text="working on request")

            web_client.chat_postMessage(
                channel=channel, blocks=prepare_message("pong", f"{time() - start}")
            )


@slack.RTMClient.run_on(event="hello")
def connected(**payload):
    web_client, rtm_client, channel, user, text = payload_parser(payload)
    web_client.chat_postMessage(channel=BOT_CHANNEL_ID, text="connected.")


rtm_client = slack.RTMClient(token=TOKEN)
print("starting...")
rtm_client.start()
print("ending.")
