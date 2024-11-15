# oot-analog-overlay
Displays your left analog stick position, with coloring to indicate you are in ess position for oot glitches. You can grab a pre-built exe from the [Releases Section](https://github.com/castlez/oot-analog-overlay/releases)

## Usage

Double click the exe and notice the two 0s appear on your screen. These are the x and y coordinates of the left analog stick. With the application focused (little snake icon in task bar) you can hold left control to move it around.

In the same dir as the exe is a config.txt with two lines describing x positions (first number) for the left analog stick: the first line is the lower bound for ESS position and the second line is the upper bound. If you leave the default there will be no coloring and it will always show the stick position in white. 

You can experiment with where your ESS bounds are and update these values accordingly (for instance, on my controller the lower bound is about 33 and my upper bound is about 42)
If the numbers are green, that means you are in ESS position!

## Build

Double click build.bat and pray
