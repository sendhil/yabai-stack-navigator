from yabai_stack_navigator.yabai_layout_details import YabaiLayoutDetails
from unittest.mock import Mock, MagicMock


def test_get_space_info_uses_correct_parameters():
    mock = Mock()
    layout_details = YabaiLayoutDetails(yabai_provider=mock)

    layout_details.get_space_info()

    mock.call_yabai.assert_called_once_with(
        ["-m", "query", "--spaces", "--space"])


def test_get_data_for_windows_in_space_passes_index():
    mock = Mock()
    layout_details = YabaiLayoutDetails(yabai_provider=mock)
    test_index = "test_index"

    layout_details.get_data_for_windows_in_space(test_index)

    mock.call_yabai.assert_called_once_with(
        ["-m", "query", "--windows", "--space", test_index])


def test_is_layout_stacked():
    data_with_stack = {"type": "stack"}
    data_without_stack = {"type": "window"}

    layout_details = YabaiLayoutDetails()

    layout_details.get_space_info = MagicMock(return_value=data_with_stack)
    assert (layout_details.is_layout_stacked())

    layout_details.get_space_info = MagicMock(return_value=data_without_stack)
    assert (not layout_details.is_layout_stacked())


def test_get_layout_index():
    data = {"index": 5}

    layout_details = YabaiLayoutDetails()

    assert (layout_details.get_layout_index(data) == data["index"])


def test_sort_stack_windows_sorts_by_stack_index():
    test_data = [
        {
            "id": 3,
            "stack-index": 3
        },
        {
            "id": 2,
            "stack-index": 2
        },
        {
            "id": 1,
            "stack-index": 1
        },
    ]

    layout_details = YabaiLayoutDetails()
    results = layout_details.sort_stacked_windows(test_data)

    assert (len(results) == 3)
    assert (results[0]["id"] == 1)
    assert (results[1]["id"] == 2)
    assert (results[2]["id"] == 3)


def test_filter_windows():
    test_data = [
        {
            "window_id": 1,
            "app": "VSCode"
        },
        {
            "window_id": 2,
            "app": "Hammerspoon"
        },
        {
            "window_id": 3,
            "app": "Hammerspoon"
        },
        {
            "window_id": 4,
            "app": "iTerm2"
        },
    ]

    layout_details = YabaiLayoutDetails()
    results = layout_details.filter_windows(test_data)

    assert (len(results) == 2)
    assert (results[0]["window_id"] == 1 and results[0]["app"] == "VSCode")
    assert (results[1]["window_id"] == 4 and results[1]["app"] == "iTerm2")
