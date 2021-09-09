import os
import logging
from .yabai_provider import YabaiProvider


class YabaiNavigator:
    def __init__(self, yabai_provider=YabaiProvider()):
        self.yabai_provider = yabai_provider

    def focus_on_stacked_window(self, window_id):
        logging.debug("Focusing on stacked window")
        args = ["-m", "window", "--focus", str(window_id)]
        return self.yabai_provider.call_yabai(args)

    def focus_on_window(self, next=True):
        if next:
            logging.debug("Focusing on next window")
            os.system(
                "yabai -m window --focus stack.next || yabai -m window --focus next || yabai -m window --focus first"
            )
        else:
            logging.debug("Focusing on previous window")
            os.system(
                "yabai -m window --focus stack.prev || yabai -m window --focus prev || yabai -m window --focus last"
            )
