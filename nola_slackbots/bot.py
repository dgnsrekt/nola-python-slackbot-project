from datetime import datetime
from time import time, sleep
from . import api

import slack


def prep_message(*, title, message):  # TODO: rename prepare_slack_message
    # TODO: DRY, sep blocks for better readability
    title_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"{title}"}}
    message_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"```{message}```"}}
    return [title_block, message_block]


def payload_parser(payload):  # TODO: rename parse_payload
    data = payload.get("data")
    web_client = payload.get("web_client")
    rtm_client = payload.get("rtm_client")

    channel = data.get("channel")
    user = data.get("user")
    text = data.get("text")

    return web_client, rtm_client, channel, user, text


def check_bot_mentioned_in_text(bot_display_name_id, text):
    if bot_display_name_id in text:
        return True
    return False


def remove_bot_display_name_id_from_text(bot_display_name_id, text):
    text = text.replace(bot_display_name_id, "")
    return text


def send_ping_message(web_client, channel, start_time=time()):  # TODO: send_ping_response
    message_block = prep_message(title="PING TEST", message=f"pong, {time() - start_time}ms")
    web_client.chat_postMessage(channel=channel, blocks=message_block)


def send_song_response(web_client, channel, topic):
    song = api.song(topic)
    for line in song:
        sleep(0.5)
        if line:
            web_client.chat_postMessage(channel=channel, text=line)


def bot_creater(*, token, bot_channel_id, bot_display_name_id, topic, title_line_number):
    # TODO: rename bot_creator
    @slack.RTMClient.run_on(event="message")
    def respond(**payload):
        start_time = time()  # Used for ping test.

        web_client, rtm_client, channel, user, text = payload_parser(payload)

        if user:
            if bot_display_name_id in text:
                text = text.replace(bot_display_name_id, "")

                if "ping" in text:
                    send_ping_message(web_client, channel, start_time=start_time)

                elif "sing" in text:
                    send_song_response(web_client, channel, topic)

                else:
                    response = api.answer_question(topic, text)  # TODO: rename answer
                    if response:
                        title, messages = api.parse_response(
                            response, title_line_number=title_line_number, max_characters=2000
                        )  # TODO: rename messages to sections

                        # TODO: rename messages to sections
                        for idx, message in enumerate(messages):
                            # TODO: rename title
                            section = f"{title} - {idx + 1} of {len(messages)}"
                            message_block = prep_message(title=section, message=message)
                            web_client.chat_postMessage(channel=channel, blocks=message_block)

                    else:
                        message_block = prep_message(title="404", message="[Subject Not Found]")
                        web_client.chat_postMessage(channel=channel, blocks=message_block)

    return slack.RTMClient(token=token)
