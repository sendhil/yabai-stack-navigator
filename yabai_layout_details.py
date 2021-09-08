from yabai_provider import YabaiProvider


class YabaiLayoutDetails:
    AppsToFilterOut = set(["Hammerspoon"])

    def __init__(self, yabai_provider=YabaiProvider()):
        self.yabai_provider = yabai_provider

    def get_space_info(self):
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--spaces", "--space"])

    def get_data_for_windows_in_space(self, index):
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--windows", "--space",
             str(index)])

    def is_layout_stacked(self):
        return self.get_space_info()["type"] == "stack"

    def get_layout_index(self, layout_data):
        return layout_data["index"]

    def sort_stacked_windows(self, window_data):
        sorted_window_data = sorted(window_data,
                                    key=lambda i: i['stack-index'])
        return sorted_window_data

    def filter_windows(self, window_data):
        return [
            window for window in window_data
            if window["app"] not in YabaiLayoutDetails.AppsToFilterOut
        ]
