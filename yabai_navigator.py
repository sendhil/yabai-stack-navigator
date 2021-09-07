#!/usr/bin/env python3

import sys
import argparse
import os
import subprocess
import json


def call_yabai(args, return_data=True):
    if return_data:
        return json.loads(
            subprocess.run(args,
                           stdout=subprocess.PIPE).stdout.decode('utf-8'))
    else:
        subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')


def get_space_info():
    return call_yabai(["yabai", "-m", "query", "--spaces", "--space"])


def get_data_for_windows_in_space(index):
    return call_yabai(
        ["yabai", "-m", "query", "--windows", "--space",
         str(index)])


# TODO: Rename
def focus_on_stacked_window(window_id):
    return call_yabai(["yabai", "-m", "window", "--focus",
                       str(window_id)],
                      return_data=False)


def focus_on_window(next=True):
    if next:
        os.system(
            "yabai -m window --focus stack.next || yabai -m window --focus next || yabai -m window --focus first"
        )
    else:
        os.system(
            "yabai -m window --focus stack.prev || yabai -m window --focus prev || yabai -m window --focus last"
        )


# Data Retrieval


def is_layout_stacked(layout_data):
    return layout_data["type"] == "stack"


def get_layout_index(layout_data):
    return layout_data["index"]


def get_focused_window(window_data):
    for window in window_data:
        if window["focused"] == 1:
            return window


def sort_stacked_windows(window_data):
    sorted_window_data = sorted(window_data, key=lambda i: i['stack-index'])
    return sorted_window_data


# TODO: Make this more customizable
def remove_hammerspoon_windows(window_data):
    return [window for window in window_data if window["app"] != "Hammerspoon"]


def get_previous_and_next_windows(sorted_window_data):
    number_of_windows = len(sorted_window_data)
    for index, window in enumerate(sorted_window_data):
        if window["focused"] == 1:
            next_window_index = (index + 1) % number_of_windows
            previous_window_index = (index - 1) % number_of_windows
            return {
                "previous_window": sorted_window_data[previous_window_index],
                "next_window": sorted_window_data[next_window_index]
            }

    raise Exception("Shoudln't get here")


def utility_get_windows(space_data):
    index = get_layout_index(space_data)
    all_window_data = get_data_for_windows_in_space(index)
    sorted_window_data = sort_stacked_windows(
        remove_hammerspoon_windows(all_window_data))
    return get_previous_and_next_windows(sorted_window_data)


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

space_data = get_space_info()
is_stacked = is_layout_stacked(space_data)

if args['debug']:
    # TODO: Clean this up to lean on `utility_get_windows`
    index = get_layout_index(space_data)
    all_window_data = get_data_for_windows_in_space(index)
    window_info = get_focused_window(all_window_data)
    sorted_window_data = sort_stacked_windows(
        remove_hammerspoon_windows(all_window_data))
    print(json.dumps(sorted_window_data, indent=4, sort_keys=True))
    sys.exit()

if is_stacked:
    window_navigation_data = utility_get_windows(space_data)

    # TODO: Simplify
    if args['next']:
        focus_on_stacked_window(window_navigation_data["next_window"]["id"])
    elif args['previous']:
        focus_on_stacked_window(
            window_navigation_data["previous_window"]["id"])
    else:
        raise Exception("Should not get here")
else:

    if args['next']:
        focus_on_window()
    elif args['previous']:
        focus_on_window(next=False)
    else:
        raise Exception("Should not get here")
