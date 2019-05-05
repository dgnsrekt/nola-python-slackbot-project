from nola_slackbots.api import remove_puctuation, replace_spaces, clean_text


def test_remove_puctuation():
    pre_text = "What is a String?!@#$%^&*()_.~`{}[]:;<.>.?/|"
    text = remove_puctuation(pre_text)
    assert text == "What is a String"


def test_replace_spaces():
    pre_text = "What is a String?"
    text = replace_spaces(pre_text)
    assert text == "What+is+a+String?"


def test_clean_text():
    pre_text = "What is a String?!@#$%^&*()_.~`{}[]:;<.>.?/|"
    text = clean_text(pre_text)
    assert text == "what+is+a+string"
