import os
from yabai_provider import YabaiProvider


class YabaiNavigator:
    def __init__(self, yabai_provider=YabaiProvider()):
        self.yabai_provider = yabai_provider

    # TODO: Rename
    def focus_on_stacked_window(self, window_id):
        return self.yabai_provider.call_yabai(
            ["yabai", "-m", "window", "--focus",
             str(window_id)],
            return_data=False)

    def focus_on_window(self, next=True):
        if next:
            os.system(
                "yabai -m window --focus stack.next || yabai -m window --focus next || yabai -m window --focus first"
            )
        else:
            os.system(
                "yabai -m window --focus stack.prev || yabai -m window --focus prev || yabai -m window --focus last"
            )
