import logging
from yabai_stack_navigator.yabai_provider import YabaiProvider


class YabaiLayoutDetails:
    AppsToFilterOut = set(["Hammerspoon", "Kap"])

    def __init__(self, yabai_provider=YabaiProvider()):
        self.yabai_provider = yabai_provider

    def get_space_info(self):
        logging.debug("Called get_space_info")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--spaces", "--space"])

    def get_space_info_for_display(self, display_index):
        logging.debug("Called get_space_info_for_display")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--spaces", "--display", str(display_index)])

    def get_display_info(self):
        logging.debug("Called get_display_info")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--displays"])

    def get_current_display_info(self):
        logging.debug("Called get_current_display_info")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--displays", "--display"])

    def get_data_for_windows_in_current_space(self):
        logging.debug("Called get_data_for_windows_in_current_space")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--windows", "--space"])

    def get_windows_for_display(self, display_index):
        logging.debug("Called get_windows_for_display")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--windows", "--display", str(display_index)])

    def get_focused_window_index(self, windows):
        for index, window in enumerate(windows):
            if window["has-focus"]:
                return index
        logging.error("Could not find current window")
        raise "Could not find current window"

    def get_data_for_windows_in_space(self, index):
        logging.debug("Called get_data_for_windows_in_space")
        return self.yabai_provider.call_yabai(
            ["-m", "query", "--windows", "--space",
             str(index)])

    def is_layout_stacked(self):
        logging.debug("Called is_layout_stacked")
        return self.get_space_info()["type"] == "stack"

    def get_layout_index(self, layout_data):
        logging.debug("Called get_layout_index")
        return layout_data["index"]

    def sort_stacked_windows(self, window_data):
        logging.debug("Called sort_stacked_windows")
        logging.debug(f"Data Before Sort: {window_data}")
        sorted_window_data = sorted(window_data,
                                    key=lambda i: i['stack-index'])
        logging.debug(f"Data After Sort: {sorted_window_data}")
        return sorted_window_data

    def filter_windows(self, window_data):
        logging.debug("Called filter_windows")
        return [
            window for window in window_data
            if window["app"] not in YabaiLayoutDetails.AppsToFilterOut
        ]
