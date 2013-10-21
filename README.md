## VintageLines v0.5
### Jankily making relative line numbers in [Vintage mode](http://www.sublimetext.com/docs/2/vintage.html)

VintageLines is available via [Sublime Package Control](http://wbond.net/sublime_packages/package_control). **Now compatible with ST3!**


#### Relative lines in command mode
![Relative lines in command mode](https://raw.github.com/tmanderson/VintageLines/master/screenshots/screenshot1.png)

#### Normal lines in insert mode
![Normal line numbers in insert mode](https://raw.github.com/tmanderson/VintageLines/master/screenshots/screenshot2.png)

### Notes

If you prefer to always have relative line numbers on set the setting "vintage_lines.force_mode": true.

If you prefer a key binding toggle relative lines on and off you can set one up by using key binding code like the following:

        {"keys": ["ctrl+t"], "command": "toggle_setting", "args": {"setting": "vintage_lines.force_mode"}}

Note that you should also set vintage_lines.force_mode in your User Preferences to your preferred default
for the toggle to be effective in both command mode and insert mode.

### CONTRIBUTORS (THANKS A LOT!):
- [@kuroir](https://github.com/kuroir)
- [@quarnster](https://github.com/quarnster)
- [@i-akhmadullin](https://github.com/i-akhmadullin)
- [@dsmatter](https://github.com/dsmatter)
