#!/usr/bin/env python3

import sys
import argparse
import os
import json
from typing import Any, Dict
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


class YabaiNavigator:
    def __init__(self,
                 yabai_provider=YabaiProvider(),
                 layout_details=YabaiLayoutDetails()):
        self.yabai_provider = yabai_provider
        self.layout_details = layout_details

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
        index = self.layout_details.get_layout_index(space_data)
        all_window_data = self.layout_details.get_data_for_windows_in_space(
            index)
        #TODO - SImplify this
        sorted_window_data = self.sort_stacked_windows(
            self.remove_hammerspoon_windows(all_window_data))
        return self.get_previous_and_next_windows(sorted_window_data)


def parse_arg_data() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--next", action="store_true", help="next window")
    group.add_argument("-p",
                       "--previous",
                       action="store_true",
                       help="previous window")
    group.add_argument("-d",
                       "--debug",
                       action="store_true",
                       help="print out some data to help with debugging")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = vars(parser.parse_args())

    return args


def print_debug_info():
    navigator = YabaiNavigator()
    layout_details = YabaiLayoutDetails()
    # TODO: Clean this up to lean on `utility_get_windows`
    index = layout_details.get_layout_index(space_data)
    all_window_data = layout_details.get_data_for_windows_in_space(index)
    sorted_window_data = navigator.sort_stacked_windows(
        navigator.remove_hammerspoon_windows(all_window_data))
    print(json.dumps(sorted_window_data, indent=4, sort_keys=True))

    sys.exit()


if __name__ == "__main__":
    args = parse_arg_data()

    navigator = YabaiNavigator()
    layout_details = YabaiLayoutDetails()

    space_data = layout_details.get_space_info()
    is_stacked = layout_details.is_layout_stacked(space_data)

    if args['debug']:
        print_debug_info()

    if is_stacked:
        window_navigation_data = navigator.utility_get_windows(space_data)
        window_key = "next_window" if args['next'] else "previous_window"
        if not args['next'] and not args['previous']:
            raise Exception("Should not get here")
        navigator.focus_on_stacked_window(
            window_navigation_data[window_key]["id"])
    else:
        if args['next']:
            navigator.focus_on_window()
        elif args['previous']:
            navigator.focus_on_window(next=False)
        else:
            raise Exception("Should not get here")
