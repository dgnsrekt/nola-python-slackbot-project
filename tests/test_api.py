from nola_slackbots.api import remove_puctuation, replace_spaces, clean_text


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
