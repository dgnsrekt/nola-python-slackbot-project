"""Provides helper functions that clean, parse, and prepare text for making web requests."""
# pylint: disable=import-error

# Standard Lib imports
import string
from typing import Optional

# Project imports
from .keywords import PYTHON_KEYWORDS
from requests_html import HTMLSession, HTMLResponse, Element


def remove_puctuation(text: str) -> str:
    """Removes punctuation from given text.

    :param text: The text to be formatted.
    returns: Text with all punctuation removed.
    """
    return text.translate(str.maketrans("", "", string.punctuation))


def replace_spaces(text: str) -> str:
    """Replaces spaces with '+' in given text.

    :param text: The text to be formatted.
    returns: Text with spaces replaced with '+'.
    """
    return text.replace(" ", "+")


def clean_text(text: str) -> str:
    """Cleans text for request.
    Removes punctuation, replaces spaces with '+', and
    converts text to lowercase.

    :param text: The text to be cleaned.
    returns: Cleaned lowercase text.
    """
    text = remove_puctuation(text)
    text = replace_spaces(text)
    return text.lower()


def prepare_request(topic: str, subtopic: str, keywords: dict = None) -> str:
    """Prepares a clean url with topic and subtopic.

    :param topic: The topic to be searched. Example: python
    :param subtopic: A subtopic in the topic. Example: print+statement
    :param keywords: A dictionary of common subtopics.
    returns: A formatted url.
    """
    url = "http://cheat.sh"
    subtopic = clean_text(subtopic)
    if keywords:
        if subtopic in keywords.keys():
            subtopic = keywords[subtopic]
    return f"{url}/{topic}/{subtopic}"


def prepare_raw_request(topic: str, subtopic: str) -> str:
    """Prepares a raw url with topic and subtopic.

    :param topic: The topic to be searched. Example: python
    :param subtopic: A subtopic of the topic. Example: print+statement
    :param keywords: A dictionary of common subtopics.
    returns: A formatted url.
    """
    url = "http://cheat.sh"
    return f"{url}/{topic}/{subtopic}"


def send_request(url: str) -> HTMLResponse:
    """Makes a http requests to the server.

    :param url: The url to send the get requests.
    returns: The html response from the server.
    """
    session = HTMLSession()
    return session.get(url)


def python_question(subtopic: str) -> Optional[str]:
    """Answers a question about python.

    :param subtopic:  A subtopic of python.
    returns: The full text string of the response or None.
    """
    pre_request = prepare_request("python", subtopic, keywords=PYTHON_KEYWORDS)
    response = send_request(pre_request)
    if response.status_code == 200:
        return response.html.find("pre", first=True).full_text

    for req in [f"{subtopic.capitalize()}", f":{subtopic}", f":{subtopic.capitalize()}"]:
        retry_pre_req = prepare_raw_request("python", req)
        response = send_request(retry_pre_req)

        if response.status_code == 200:
            return response.html.find("pre", first=True).full_text

    return None


def bash_question(subtopic: str) -> Optional[str]:
    """Answers a question about bash.

    :param subtopic:  A subtopic of bash.
    returns: The full text string of the response or None.
    """

    pre_request = prepare_request("bash", subtopic)
    response = send_request(pre_request)
    if response.status_code == 200:
        return response.html.find("pre", first=True).full_text
    return None


def git_question(subtopic: str) -> Optional[str]:
    """Answers a question about qit.

    :param subtopic:  A subtopic of git.
    returns: The full text string of the response or None.
    """

    pre_request = prepare_request("git", subtopic)
    response = send_request(pre_request)
    if response.status_code == 200:
        return response.html.find("pre", first=True).full_text
    return None


def answer_question(topic: str, subtopic: str) -> Element:
    """Helper function which blah
    """
    topics = {"python": python_question, "git": git_question, "bash": bash_question}
    return topics[topic](subtopic)


def parse_response(full_text_response, title_line_number=1, max_characters=1500):
    chunks = str()
    messages = list()

    title = full_text_response.split("\n")[title_line_number].strip("#").lstrip()

    def is_newline_character(char):
        if char == "\n":
            return True
        return False

    for char in full_text_response:
        chunks += char
        if len(chunks) > max_characters:
            if is_newline_character(char):
                messages.append(chunks)
                chunks = str()

    messages.append(chunks)

    return title, messages


def print_messages(title, messages):
    for i, message in enumerate(messages):
        print("Request:", title)
        print("=" * 50, f"section {(i) + 1} of {len(messages)}", "=" * 50)
        print(message)


def python_song():
    url = (
        "https://gist.githubusercontent.com/dgnsrekt/03c49575c6c0b0aa49c84a1d70e9e735"
        "/raw/1236a06bc34f389c8d1bec6963ccdc0d470291b2/mr-python-song"
    )
    response = send_request(url)
    if response.status_code == 200:
        return response.html.full_text.split("\n")
    return None


def git_song():
    url = (
        "https://gist.githubusercontent.com/dgnsrekt/3af28a1848c961c0a031287e9311f2b9"
        "/raw/ab5da67401b98ad8a713cb3680ccafdcef690e96/gitman-song"
    )
    response = send_request(url)
    if response.status_code == 200:
        return response.html.full_text.split("\n")
    return None


def bash_song():
    url = (
        "https://gist.githubusercontent.com/dgnsrekt/29c630b9a2069388f5e9b3378f74a8da"
        "/raw/a23a8c25f36c1f62b2dc4a0a70689030f7516311/unix-terminator"
    )
    response = send_request(url)
    if response.status_code == 200:
        return response.html.full_text.split("\n")
    return None


def song(topic):  # Return 404 or raise error
    songs = {"python": python_song, "git": git_song, "bash": bash_song}
    return songs[topic]()
