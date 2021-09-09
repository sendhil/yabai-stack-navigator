from yabai_stack_navigator.yabai_stacked_window_provider \
     import YabaiStackedWindowProvider
from unittest.mock import Mock


def base_test_data():
    return [
        {
            "focused": 0,
            "id": 1
        },
        {
            "focused": 0,
            "id": 2
        },
        {
            "focused": 0,
            "id": 3
        },
    ]


# Check the scenario when we're navigating from the middle
def test_get_previous_and_next_windows_middle_node():
    mock = Mock()
    test_data = base_test_data()
    test_data[1]["focused"] = 1
    mock.sort_stacked_windows.return_value = test_data
    provider = YabaiStackedWindowProvider(layout_details=mock)

    results = provider.get_previous_and_next_windows()

    assert (results["previous_window"]['id'] == 1)
    assert (results["next_window"]['id'] == 3)


# Check the scenario when we're navigating from the first window
def test_get_previous_and_next_windows_head_node():
    mock = Mock()
    test_data = base_test_data()
    test_data[0]["focused"] = 1
    mock.sort_stacked_windows.return_value = test_data
    provider = YabaiStackedWindowProvider(layout_details=mock)

    results = provider.get_previous_and_next_windows()

    assert (results["previous_window"]['id'] == 3)
    assert (results["next_window"]['id'] == 2)


# Check the scenario when we're navigating from the last window
def test_get_previous_and_next_windows_tail_node():
    mock = Mock()
    test_data = base_test_data()
    test_data[2]["focused"] = 1
    mock.sort_stacked_windows.return_value = test_data
    provider = YabaiStackedWindowProvider(layout_details=mock)

    results = provider.get_previous_and_next_windows()

    assert (results["previous_window"]['id'] == 2)
    assert (results["next_window"]['id'] == 1)


def test_get_previous_and_next_windows_throws_exception():
    mock = Mock()
    test_data = base_test_data()
    mock.sort_stacked_windows.return_value = test_data
    provider = YabaiStackedWindowProvider(layout_details=mock)

    try:
        provider.get_previous_and_next_windows()
    except Exception as e:
        assert (e is not None)
        assert ("Shoudln't" in str(e))
