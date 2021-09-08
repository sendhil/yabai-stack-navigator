import json
import subprocess


# TODO: Include "yabai" as an already included argument
class YabaiProvider:
    """Class to abstract out calling out to Yabai"""
    def call_yabai(self, args, return_data=True):
        if args[0] != "yabai":
            args = ["yabai"] + args

        if return_data:
            return json.loads(
                subprocess.run(args,
                               stdout=subprocess.PIPE).stdout.decode('utf-8'))
        else:
            subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')