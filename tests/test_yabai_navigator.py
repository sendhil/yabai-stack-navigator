from yabai_stack_navigator.yabai_navigator import YabaiNavigator
from unittest.mock import Mock, patch


def test_focus_on_stacked_window_passes_in_window_id():
    mock = Mock()
    test_window_id = "test_window_id"

    navigator = YabaiNavigator(yabai_provider=mock)
    navigator.focus_on_stacked_window(test_window_id)

    mock.call_yabai.assert_called_with(
        ["-m", "window", "--focus", test_window_id])


@patch('os.system')
def test_focus_on_window_uses_next(mock_os):
    navigator = YabaiNavigator()
    navigator.focus_on_window(next=True)
    mock_os.assert_called_once()
    assert ("next" in mock_os.call_args[0][0])


@patch('os.system')
def test_focus_on_window_uses_previous(mock_os):
    navigator = YabaiNavigator()
    navigator.focus_on_window(next=False)

    mock_os.assert_called_once()
    assert ("prev" in mock_os.call_args[0][0])
