from yabai_stack_navigator.yabai_layout_details import YabaiLayoutDetails


class YabaiStackedWindowProvider:
    def __init__(self, layout_details=YabaiLayoutDetails()):
        self.layout_details = layout_details

    def get_previous_and_next_windows(self):
        space_data = self.layout_details.get_space_info()
        index = self.layout_details.get_layout_index(space_data)
        all_window_data = self.layout_details.get_data_for_windows_in_space(
            index)
        # This is to primarily remove Hammerspoon which shows up as
        # a part of the layout details in Yabai
        filtered_window_data = self.layout_details.filter_windows(
            all_window_data)
        sorted_window_data = self.layout_details.sort_stacked_windows(
            filtered_window_data)

        number_of_windows = len(sorted_window_data)
        for index, window in enumerate(sorted_window_data):
            if self._is_window_focused(window):
                next_window_index = (index + 1) % number_of_windows
                previous_window_index = (index - 1) % number_of_windows
                return {
                    "previous_window":
                    sorted_window_data[previous_window_index],
                    "next_window": sorted_window_data[next_window_index]
                }

        raise Exception("Shoudln't get here")

    def _is_window_focused(self, window):
        # Yabai added breaking changes to it's data format in version 4.0.
        # This method just works around those changes and maintains backwards compatability.
        if "focused" in window:
            return window["focused"]
        elif "has-focus" in window:
            return window["has-focus"]
        else:
            raise "Focus key not found"
