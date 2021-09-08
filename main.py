#!/usr/bin/env python3

import sys
import argparse
import json
from typing import Any, Dict
from yabai_layout_details import YabaiLayoutDetails
from yabai_navigator import YabaiNavigator
from yabai_stacked_window_provider import YabaiStackedWindowProvider


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
    space_data = layout_details.get_space_info()
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
    stacked_window_provider = YabaiStackedWindowProvider()

    if args['debug']:
        print_debug_info()

    if layout_details.is_layout_stacked():
        window_navigation_data = stacked_window_provider.get_previous_and_next_windows(
        )
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
