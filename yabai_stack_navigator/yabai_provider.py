import json
import subprocess
import logging
from typing import Any


class YabaiProvider:
    """Class to abstract out calling out to Yabai"""
    def call_yabai(self, args) -> Any:
        if args[0] != "yabai":
            args = ["yabai"] + args

        logging.debug(f"Calling Yabai With Args: {args}")
        command_output = subprocess.run(
            args, stdout=subprocess.PIPE).stdout.decode('utf-8')

        if len(command_output) > 0:
            logging.debug(f"Output from Yabai: {command_output}")
            return json.loads(command_output)
        else:
            logging.debug("No output from Yabai")
            return None
