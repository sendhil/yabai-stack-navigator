from yabai_layout_details import YabaiLayoutDetails


class YabaiStackedWindowProvider:
    def __init__(self, layout_details=YabaiLayoutDetails()):
        self.layout_details = layout_details

    def get_previous_and_next_windows(self):
        space_data = self.layout_details.get_space_info()
        index = self.layout_details.get_layout_index(space_data)
        all_window_data = self.layout_details.get_data_for_windows_in_space(
            index)
        # We remove hammerspoon windows because they show up as a part of the layout details in Yabai
        filtered_window_data = self.layout_details.remove_hammerspoon_windows(
            all_window_data)
        sorted_window_data = self.layout_details.sort_stacked_windows(
            filtered_window_data)

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