from utils import add_sorting_keys, contains_words


def test_contains_words_is_case_insensitive():
    assert contains_words("Data Analyst", ["data"])
    assert not contains_words("Marketing Intern", ["analytics"])


def test_add_sorting_keys_marks_relevance_and_negative_terms_win():
    jobs = {
        "positive": {"title": "Data Analyst"},
        "negative": {"title": "Data Analyst Praktikum"},
        "neutral": {"title": "Sales Associate"},
    }

    result = add_sorting_keys(jobs, ["data", "analyst"], ["praktikum"])

    assert result is jobs
    assert jobs["positive"]["relevance"] == 1
    assert jobs["positive"]["font_style"] == 'style="color:green;"'
    assert jobs["negative"]["relevance"] == -1
    assert jobs["negative"]["font_style"] == 'style="color:purple;"'
    assert jobs["neutral"]["relevance"] == 0
    assert jobs["neutral"]["font_style"] == ""