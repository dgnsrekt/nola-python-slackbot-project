from datetime import datetime
from time import time, sleep
import api

import slack


def prep_message(*, title, message):
    title_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"{title}"}}
    message_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"```{message}```"}}
    return [title_block, message_block]


def payload_parser(payload):
    data = payload.get("data")
    web_client = payload.get("web_client")
    rtm_client = payload.get("rtm_client")

    channel = data.get("channel")
    user = data.get("user")
    text = data.get("text")

    return web_client, rtm_client, channel, user, text


def bot_creater(*, token, bot_channel_id, bot_display_name, song_name, title_line_number):
    @slack.RTMClient.run_on(event="message")
    def ping(**payload):
        start = time()

        web_client, rtm_client, channel, user, text = payload_parser(payload)
        if user:
            if bot_display_name in text:
                text = text.replace(bot_display_name, "")

                if "ping" in text:
                    message_block = prep_message(title="pong", message=f"{time() - start}")
                    web_client.chat_postMessage(channel=channel, blocks=message_block)

                elif "sing" in text:
                    song = api.song(song_name)
                    for line in song:
                        sleep(0.5)
                        if line:
                            web_client.chat_postMessage(channel=channel, text=line)

                else:
                    response = api.bash_question(text)
                    title, messages = api.parse_response(
                        response, title_line_number=title_line_number, max_characters=2000
                    )

                    for idx, message in enumerate(messages):
                        section = f"{title} - {idx + 1} of {len(messages)}"
                        message_block = prep_message(title=section, message=message)
                        web_client.chat_postMessage(channel=channel, blocks=message_block)

    return slack.RTMClient(token=token)
