import json
import subprocess
from typing import Any


# TODO: Include "yabai" as an already included argument
class YabaiProvider:
    """Class to abstract out calling out to Yabai"""
    def call_yabai(self, args) -> Any:
        if args[0] != "yabai":
            args = ["yabai"] + args

        return json.loads(
            subprocess.run(args,
                           stdout=subprocess.PIPE).stdout.decode('utf-8'))
