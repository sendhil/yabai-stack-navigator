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


