from mavis_reporting.helpers import url_helper


def example_dict():
    return {
        "key1": "value 1",
        "key2": "value 2",
        "complex_key": {"complex_key_sub_1": "aaa", "complex_key_sub_2": "bbb"},
    }


def test_dict_without_keys_with_a_single_simple_key_removes_the_correct_key(app):
    assert url_helper.dict_without_keys(example_dict(), "key2") == {
        "key1": "value 1",
        "complex_key": {"complex_key_sub_1": "aaa", "complex_key_sub_2": "bbb"},
    }


def test_dict_without_keys_with_multiple_simple_keys_removes_the_correct_keys(app):
    assert url_helper.dict_without_keys(example_dict(), ["key1", "key2"]) == {
        "complex_key": {"complex_key_sub_1": "aaa", "complex_key_sub_2": "bbb"},
    }


def test_dict_without_keys_with_a_single_complex_key_removes_the_correct_key(app):
    assert url_helper.dict_without_keys(example_dict(), "complex_key") == {
        "key1": "value 1",
        "key2": "value 2",
    }


def test_dict_without_keys_with_a_mix_of_simple_and_complex_keys_removes_the_correct_keys(
    app,
):
    assert url_helper.dict_without_keys(example_dict(), ["key1", "complex_key"]) == {
        "key2": "value 2"
    }


def test_url_without_param_with_a_single_param_removes_the_param(app):
    assert (
        url_helper.url_without_param(
            "https://some.domain/path/file.name?q=search+string", "q"
        )
        == "https://some.domain/path/file.name"
    )


def test_url_without_param_with_multiple_params_removes_the_correct_param(app):
    assert (
        url_helper.url_without_param(
            "https://some.domain/path/file.name?q=search%20string&other_param=othervalue",
            "q",
        )
        == "https://some.domain/path/file.name?other_param=othervalue"
    )


def test_url_without_param_with_multiple_other_params_preserves_the_order_of_params_which_are_not_removed(
    app,
):
    assert (
        url_helper.url_without_param(
            "https://some.domain/path/file.name?q=search%20string&b=bbb&a=aaa",
            "q",
        )
        == "https://some.domain/path/file.name?b=bbb&a=aaa"
    )


def test_url_without_param_with_a_single_param_that_is_not_present_makes_no_changes(
    app,
):
    assert (
        url_helper.url_without_param(
            "https://some.domain/path/file.name?q=search+string&b=bbb&a=aaa&", "c"
        )
        == "https://some.domain/path/file.name?q=search+string&b=bbb&a=aaa&"
    )
