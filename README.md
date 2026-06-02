# About this project
I've been around the block enough times to know that there's always a few things that I always go in and fix in every project I have, so I might as well make a copy/pastable template for it. You can use it too if you want.
## Usage
Copy the contents of this project when you want to start a new project, instead of using the button in the renpy sdk.

For the most part, the configuration variables you'll want to change are in `definitions.rpy`.
## Key Changes
- Sensible `.gitignore` file
- Added default style to all buttons that gives them `activate_sound` and `hover_sound` parameters
- Added transform `hover_nav` to all buttons in `navigation()`
- Most importantly: prevented accidental activation of `hover_sound` when clicking navigation_menu items and changing screens.

## Future Changes
Subject to my changing whims.
- Better nvl mode defaults
- Refactor some configuration variables
- Fix selection attribute on "fullscreen mode" button
