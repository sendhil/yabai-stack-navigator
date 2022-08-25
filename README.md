# Yabai Stack Navigator

A simple script to make navigating between stacks and windows in [Yabai](https://github.com/koekeishiya/yabai) easier. I wrote this as I wanted to be able to use the same keyboard shortcut to navigate between windows and stacks. I found some options listed in [this](https://github.com/koekeishiya/yabai/issues/203) issue but they didn't quite do everything I wanted (specifically rotate at the end of the stacks).

# Installation

```
pip install yabai-stack-navigator
```

# Usage

Call the script with `--next` or `--previous` and it'll navigate to the appropriate window/stack. I use [skhd](https://github.com/koekeishiya/skhd) and my setup looks like:

```
alt - h : yabai-stack-navigator --prev
alt - l : yabai-stack-navigator --next
```

Here's a video of this in action (note, I use the [Stackline](https://github.com/AdamWagner/stackline) to help with visualizing stacks). 

![yabai stack navigator](https://user-images.githubusercontent.com/437043/132923238-e103370c-3bd8-43ba-8f01-45f451ce4f40.gif)


# Changes

## 1.0.7

- Added ability to navigate between displays (except when encountering a stack).

## 1.0.6

- Being a relative Python newbie, I made a mistake in the way I setup the CLI and it resulted in the main.py being added to the root folder of `site-packages`. Upgrading to this version should fix this, but you can double check by seeing if `main.py` in the python `site-packages` folder(e.g. `/opt/homebrew/lib/python3.x/site-packages/main.py`) matches [this](https://github.com/sendhil/yabai-stack-navigator/blob/7986767f48e4e26afbdca627c58df11658637e32/main.py) code and if it does please remove it. Sorry for the inconvenience.