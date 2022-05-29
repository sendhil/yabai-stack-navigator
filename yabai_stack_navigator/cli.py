#!/usr/bin/env python3

import sys
import argparse
import logging
from typing import Any, Dict
from yabai_stack_navigator.yabai_layout_details import YabaiLayoutDetails
from yabai_stack_navigator.yabai_navigator import YabaiNavigator
from yabai_stack_navigator.yabai_stacked_window_provider \
    import YabaiStackedWindowProvider


def parse_arg_data() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--next", action="store_true", help="next window")
    group.add_argument("-p",
                       "--previous",
                       action="store_true",
                       help="previous window")
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Verbose mode to aid in debugging")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = vars(parser.parse_args())

    if args["verbose"]:
        logging.basicConfig(level=logging.DEBUG)

    return args


def main():
    args = parse_arg_data()

    navigator = YabaiNavigator()

    if YabaiLayoutDetails().is_layout_stacked():
        logging.debug("Stack layout detected")
        window_navigation_data = YabaiStackedWindowProvider(
        ).get_previous_and_next_windows()
        window_key = "next_window" if args['next'] else "previous_window"
        if not args['next'] and not args['previous']:
            raise Exception("Should not get here")
        navigator.focus_on_stacked_window(
            window_navigation_data[window_key]["id"])
    else:
        logging.debug("Non-stacked layout detected")
        if args['next']:
            navigator.focus_on_window()
        elif args['previous']:
            navigator.focus_on_window(next=False)
        else:
            raise Exception("Should not get here")


if __name__ == "__main__":
    main()