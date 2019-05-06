from nola_slackbots.api import remove_puctuation, replace_spaces, clean_text
from nola_slackbots.api import get_request, prepare_request, prepare_raw_request
import pytest


def test_remove_puctuation():
    t_before = "What is a String?!@#$%^&*()_.~`{}[]:;<.>.?/|"
    t_after = remove_puctuation(t_before)
    t_expected = "What is a String"
    assert t_after == t_expected


def test_replace_spaces():
    t_before = "What is a String?"
    t_after = replace_spaces(t_before)
    t_expected = "What+is+a+String?"
    assert t_after == t_expected


def test_clean_text():
    t_before = "What is a String?!@#$%^&*()_.~`{}[]:;<.>.?/|"
    t_after = clean_text(t_before)
    t_expected = "what+is+a+string"
    assert t_after == t_expected


def test_prepare_request():
    t_topic = "python"
    t_subtpic = "Classes"
    t_expected = "http://cheat.sh/python/classes"
    t_results = prepare_request(t_topic, t_subtpic)
    assert t_expected == t_results


def test_prepare_request_with_keywords():
    t_keywords = {"class": "Classes", "classes": "Classes"}
    t_topic = "python"
    t_subtpic = "classes"
    t_expected = "http://cheat.sh/python/Classes"
    t_results = prepare_request(t_topic, t_subtpic, t_keywords)
    assert t_expected == t_results


def test_prepare_raw_request():
    t_topic = "python"
    t_subtpic = "Classes"
    t_expected = "http://cheat.sh/python/Classes"
    t_results = prepare_raw_request(t_topic, t_subtpic)
    assert t_expected == t_results


@pytest.mark.online
def test_get_request():
    url = "https://httpbin.org"
    response = get_request(url)
    assert response.text.split("\n")[0] == "<!DOCTYPE html>"
