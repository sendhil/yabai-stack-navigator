from yabai_navigator import YabaiNavigator
from unittest.mock import Mock


def test_focus_on_stacked_window_passes_in_window_id():
    mock = Mock()
    test_window_id = "test_window_id"

    navigator = YabaiNavigator(yabai_provider=mock)
    navigator.focus_on_stacked_window(test_window_id)

    mock.call_yabai.assert_called_with(
        ["yabai", "-m", "window", "--focus", test_window_id],
        return_data=False)
