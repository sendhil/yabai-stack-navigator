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

    def is_layout_stacked(self, layout_data):
        return layout_data["type"] == "stack"

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

    def get_previous_and_next_windows(self, sorted_window_data):
        number_of_windows = len(sorted_window_data)
        for index, window in enumerate(sorted_window_data):
            if window["focused"] == 1:
                next_window_index = (index + 1) % number_of_windows
                previous_window_index = (index - 1) % number_of_windows
                return {
                    "previous_window":
                    sorted_window_data[previous_window_index],
                    "next_window": sorted_window_data[next_window_index]
                }

        raise Exception("Shoudln't get here")

    # TODO - rename split up?
    def utility_get_windows(self, space_data):
        index = self.get_layout_index(space_data)
        all_window_data = self.get_data_for_windows_in_space(index)
        # TODO - Simplify this
        sorted_window_data = self.sort_stacked_windows(
            self.remove_hammerspoon_windows(all_window_data))
        return self.get_previous_and_next_windows(sorted_window_data)
