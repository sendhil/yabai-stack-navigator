from yabai_provider import YabaiProvider


class YabaiLayoutDetails:
    def __init__(self, yabai_provider=YabaiProvider()):
        self.yabai_provider = YabaiProvider()

    def get_space_info(self):
        return self.yabai_provider.call_yabai(
            ["yabai", "-m", "query", "--spaces", "--space"])

    def get_data_for_windows_in_space(self, index):
        return self.yabai_provider.call_yabai(
            ["yabai", "-m", "query", "--windows", "--space",
             str(index)])

    def is_layout_stacked(self):
        return self.get_space_info()["type"] == "stack"

    def get_layout_index(self, layout_data):
        return layout_data["index"]

    # TODO: Remove as this might not be used
    def get_focused_window(self, window_data):
        for window in window_data:
            if window["focused"] == 1:
                return window

    def sort_stacked_windows(self, window_data):
        sorted_window_data = sorted(window_data,
                                    key=lambda i: i['stack-index'])
        return sorted_window_data

    # TODO: Make this more customizable
    def remove_hammerspoon_windows(self, window_data):
        return [
            window for window in window_data if window["app"] != "Hammerspoon"
        ]
