"""Provides helper functions that clean, parse, and prepare text for making api requests."""

import string
from requests_html import HTMLSession
from .keywords import PYTHON_COMMON_KEYWORDS, PYTHON_KEYWORDS


def remove_puctuation(text):
    """Removes all punctuation from text.

    Args:
        text: A string to be formatted.
    Returns:
        A str with all punctuation removed.
    """
    return text.translate(str.maketrans("", "", string.punctuation))


def replace_spaces(text):
    """Replaces all spaces with + for a properly formatted request.

    Args:
        text: A string to be formatted.
    Returns:
        str with spaces replaced with +.
    """
    return text.replace(" ", "+")


def clean_text(text):
    """Cleans text for properly formatted requests
    Removes punctuation, replaces spaces, and lowers the text

    Args:
        text: A string to be formatted.
    Returns:
        str clean text
    """
    text = remove_puctuation(text)
    text = replace_spaces(text)
    return text.lower()


def prepare_request(topic, subtopic, keywords=None):
    url = "http://cheat.sh"
    subtopic = clean_text(subtopic)
    if keywords:
        if subtopic in keywords.keys():
            subtopic = keywords[subtopic]
    return f"{url}/{topic}/{subtopic}"


def prepare_reformatted_request(topic, subtopic):
    url = "http://cheat.sh"
    return f"{url}/{topic}/{subtopic}"


def make_request(url):
    session = HTMLSession()
    return session.get(url)


def python_question(subtopic):
    pre_request = prepare_request("python", subtopic, keywords=PYTHON_KEYWORDS)
    response = make_request(pre_request)
    if response.status_code == 200:
        return response.html.find("pre", first=True)

    for req in [f"{subtopic.capitalize()}", f":{subtopic}", f":{subtopic.capitalize()}"]:
        retry_pre_req = prepare_reformatted_request("python", req)
        response = make_request(retry_pre_req)

        if response.status_code == 200:
            return response.html.find("pre", first=True)

    return None


def bash_question(subtopic):
    pre_request = prepare_request("bash", subtopic)
    response = make_request(pre_request)
    if response.status_code == 200:
        return response.html.find("pre", first=True)
    return None


def git_question(subtopic):
    pre_request = prepare_request("git", subtopic)
    response = make_request(pre_request)
    if response.status_code == 200:
        return response.html.find("pre", first=True)
    return None


def answer_question(system, subtopic):
    systems = {"python": python_question, "git": git_question, "bash": bash_question}
    return systems[system](subtopic)


def parse_response(resp, title_line_number=1, max_characters=1500):
    chunks = str()
    messages = list()

    title = resp.full_text.split("\n")[title_line_number].strip("#").lstrip()

    def is_newline_character(char):
        if char == "\n":
            return True

    for char in resp.full_text:
        chunks += char
        if len(chunks) > max_characters:
            if is_newline_character(char):
                messages.append(chunks)
                chunks = str()

    else:
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
    response = make_request(url)
    if response.status_code == 200:
        return response.html.full_text.split("\n")
    return None


def git_song():
    url = (
        "https://gist.githubusercontent.com/dgnsrekt/3af28a1848c961c0a031287e9311f2b9"
        "/raw/ab5da67401b98ad8a713cb3680ccafdcef690e96/gitman-song"
    )
    response = make_request(url)
    if response.status_code == 200:
        return response.html.full_text.split("\n")
    return None


def bash_song():
    url = (
        "https://gist.githubusercontent.com/dgnsrekt/29c630b9a2069388f5e9b3378f74a8da"
        "/raw/a23a8c25f36c1f62b2dc4a0a70689030f7516311/unix-terminator"
    )
    response = make_request(url)
    if response.status_code == 200:
        return response.html.full_text.split("\n")
    return None


def song(bot):
    songs = {"python": python_song, "git": git_song, "bash": bash_song}
    return songs[bot]()
