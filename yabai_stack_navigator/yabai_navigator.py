import os
import logging
from yabai_stack_navigator.yabai_provider import YabaiProvider
from yabai_stack_navigator.yabai_layout_details import YabaiLayoutDetails
from enum import Enum

class Direction(Enum):
    East = 1
    West = 2

class YabaiNavigator:
    def __init__(self, yabai_provider=YabaiProvider(), yabai_layout_details=YabaiLayoutDetails()):
        self.yabai_provider = yabai_provider
        self.yabai_layout_details = yabai_layout_details

    def focus_on_window(self, window_id):
        logging.debug("Focusing on window")
        args = ["-m", "window", "--focus", str(window_id)]
        return self.yabai_provider.call_yabai(args)

    def focus_on_display(self, display_index):
        logging.debug(f"Focusing on display : {display_index}")
        args = ["-m", "display", "--focus", str(display_index)]
        return self.yabai_provider.call_yabai(args)

    def focus_window_direction(self, direction:Direction):
        logging.debug(f"Focusing on window direction : {direction}")
        args = ["-m", "window", "--focus", "next" if direction == Direction.East else "prev"]
        return self.yabai_provider.call_yabai(args)

    def focus_on_next_window(self):
        self._handle_focus_window_in_direction(Direction.East)

    def focus_on_previous_window(self):
        self._handle_focus_window_in_direction(Direction.West)

    def _handle_focus_window_in_direction(self, direction:Direction):
        # 1. Get windows on current space
        logging.debug("Trying to find windows for the current space")
        windows_on_current_space = self.yabai_layout_details.get_data_for_windows_in_current_space()

        if not windows_on_current_space:
            logging.debug("Could not find windows on current space, going to just focus on the next display")
            next_display = self._get_next_display(direction)
            self.focus_on_display(next_display["index"])
            return

        # 2. Is there a previous/next window?
        current_window = windows_on_current_space[self.yabai_layout_details.get_focused_window_index(windows_on_current_space)]
        if self._is_there_next_window(current_window["id"], direction):
            logging.debug("Found a next window to focus on in the current space")
            self.focus_window_direction(direction)
            return

        logging.debug("Did not find a next window to focus on in the current space")

        # 3. Determine next display (i.e. east/west, or roll over)
        logging.debug("Determining next display")
        next_display = self._get_next_display(direction)

        # 4. Are there windows on next display? If so, focus on the first.
        logging.debug("Trying to find windows on next display")

        has_windows, first_window_id = self._first_window_for_display(next_display["index"])
        if has_windows:
            logging.debug(f"Found windows on next display, focusing on window {first_window_id}")
            self.focus_on_window(first_window_id)
            return

        logging.debug("Did not find windows on next display")

        # 5. Focus on next display
        logging.debug("Focusing on next display")
        self.focus_on_display(next_display["index"])

        return

    def _is_there_next_window(self, current_window_id, direction:Direction):
        space_info = self.yabai_layout_details.get_space_info()
        if len(space_info["windows"]) <= 1:
            logging.debug("_is_there_next_window: one or fewer windows, so there can't be a next window")
            return False

        if direction == Direction.East:
            return space_info["last-window"] != current_window_id
        elif direction == Direction.West:
            return space_info["first-window"] != current_window_id
        
        raise "Should not get here"

    def _get_next_display(self, direction:Direction) -> int:
        display_info = self.yabai_layout_details.get_display_info()
        sorted(display_info, key=lambda info: info["frame"]["x"])

        current_display_info = self.yabai_layout_details.get_current_display_info()
        current_display_index:Optional[int] = None
        for index, value in enumerate(display_info):
            if current_display_info["index"] == value["index"]:
                current_display_index = index
                break

        if current_display_index == None:
            logging.error("Could not find current display index")
            raise "Could not find current display index"

        delta = 1 if direction == Direction.East else -1
        next_display = display_info[(current_display_index + delta) % len(display_info)]
        logging.debug(f"Next display : {next_display}")

        return next_display

    # Returns (has_windows, window_id)
    def _first_window_for_display(self, display_index) -> (bool, int):
        space_info = self.yabai_layout_details.get_space_info_for_display(display_index)
        for item in space_info:
            if item["is-visible"]:
                return (item["first-window"] != 0, item["first-window"])

        logging.error("Could not find a visible space")
        raise "Should not get here"



