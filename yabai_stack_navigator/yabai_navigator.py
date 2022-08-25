import os
import logging
from yabai_stack_navigator.yabai_provider import YabaiProvider


class YabaiNavigator:
    def __init__(self, yabai_provider=YabaiProvider()):
        self.yabai_provider = yabai_provider

    def focus_on_stacked_window(self, window_id):
        logging.debug("Focusing on stacked window")
        args = ["-m", "window", "--focus", str(window_id)]
        return self.yabai_provider.call_yabai(args)

    def focus_on_window(self, next=True):
        # Shell commands largely based off of https://github.com/koekeishiya/yabai/issues/225#issuecomment-529520392
        if next:
            logging.debug("Focusing on next window")
            os.system(
                r"""yabai -m window --focus next || yabai -m window --focus "$((yabai -m query --spaces --display next || yabai -m query --spaces --display first) | jq -re '.[] | select(."is-visible" == true)."first-window"')" || yabai -m display --focus next || yabai -m display --focus first"""
            )
        else:
            logging.debug("Focusing on previous window")
            os.system(
                r"""yabai -m window --focus prev || yabai -m window --focus "$((yabai -m query --spaces --display prev || yabai -m query --spaces --display last) | jq -re '.[] | select(."is-visible" == true)."last-window"')" || yabai -m display --focus prev || yabai -m display --focus last"""
            )
