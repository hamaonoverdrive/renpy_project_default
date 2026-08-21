# About this project
I've been around the block enough times to know that there's always a few things that I always go in and fix in every project I have, so I might as well make a copy/pastable template for it. You can use it too if you want.
## Usage
Copy the contents of this project when you want to start a new project, instead of using the button in the renpy sdk.

For the most part, the configuration variables you'll want to change are in `definitions.rpy`.
## Key Changes
- Sensible `.gitignore` file
- Preference screen QoL tweaks
- Added default style to all buttons that gives them `activate_sound` and `hover_sound` parameters, and  adv_sound
- Added transform `hover_nav` to all buttons in `navigation()`
- Modified default nvl behavior to length, height = None
    - Also corrected the history and small screen variant
- nvl mode scrolls on overflow, optional scrollbar to go back up
- Most importantly: prevented accidental activation of `hover_sound` when clicking navigation_menu items and changing screens.

### Added to `/game/plugins`
- [kigyodev's improved word counter](https://kigyo.itch.io/renpy-word-counter)
- my homebrewed text bloop plugin

## Future Changes
Subject to my changing whims.
- Refactor some configuration variables
