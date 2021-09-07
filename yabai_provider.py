import json
import subprocess


# TODO: Not the best name, rename it as it feels a bit too .NETey
class YabaiProvider:
    """Class to abstract out calling out to Yabai"""
    def call_yabai(self, args, return_data=True):
        if return_data:
            return json.loads(
                subprocess.run(args,
                               stdout=subprocess.PIPE).stdout.decode('utf-8'))
        else:
            subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')