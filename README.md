This Trinket contains all the files you need to configure the Warp Core.

- update.py - This file needs to be copied to a computer connected via USB to the cable coming out of the Warp Core
- weather_patterns.cvs - This is the file that translates the OpenWeatherMap codes into an animation pattern
- main.py - This is what the Trinket runs. It doesn't know anything about weather, it just looks for "animations.txt" and executes (via eval()) the code in that file within the scope of its while loop

You can hand-edit animations.txt if you want to test the patterns and see how they look. "animations.txt" is placed on the Trinket's drive by "update.py". "update.py" assumes you're on Windows, and that the Trinket is the F drive. You'll have to change the path to the correct value for the Trinket by editing "update.py".

OpenWeatherMap (https://openweathermap.org) is a free API for gathering weather data for any region, and which provides the data in the units you specify (imperial, metric, etc). The report this script requests is a 5-day report, which is converted from json and passed through a filter (of sorts) to tell the lamp what animation to use.

Ultimately, the lamp just needs to be told how to animate. Weather is only one possible usage. You could write animations to "animations.txt" having to do with build status, activity monitoring, systems monitoring, home automation, or anything.

Things to improve:
- Un-hard-code the API key
- Allow the region/zip/units/etc to be parameterized, or be read from a json properties file
- More animations
- Need a better way to indicate some kind of timeframe (I'd like to know if Rain is coming any time in the next 3 hours, and if it's sooner, I'd like it to indicate that)
- Fix some more of the off-by-one errors in the lights
- Publish to github
- Figure out how to do power/logic for the whole thing with one cable, ideally USB
