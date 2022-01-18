# Robo-Animator
Test UI for animating servos on a Raspberry Pi directly from Blender animations (old project, but probably salvageable) through a socket server. 
You could probably build the whole thing on the Pi itself now come to think of it. This project was to explore the idea of automating 3d modeling and animation, and was going to be expanded to include outputs for the 3D models to a 3d printer slicer so the modeling and animation could all be done at the same time from Blender. This was built with Blender 2.7 and Python3 and could output single axis movements of your choice from an armature to a servo. We did have it working roughly, the RPi integration was a one-off test however and needs support for steppers etc. Pretty cool, right?

The other part of this project that never saw the light of day was integrating klipper support and sensor support to experiment with stabilizing higher quality 3D prints out of the software as well. Don't ask...


HOW TO USE
- Install Blender, make a simple keyframe animation with bones
- Run Testrun_server.py on the Pi
- Run roboanimator.py on the client machine

Buttons
- Edit & Import Animation opens blender with a selected .blend file, or none at all for a
blank animation. When you close this instance of blender, the app unfreezes and imports any
armature data available in that animation.
- Import animation imports data without opening blender

- Write Animation Config writes a Json file for the associated data and added flags
 flags are names like 'LED1_ON' or 'SOUNDNAME' to call an LED turning on or that sound
file by the names given in the RobotIO or Sounds tabs.

- Import Port Config imports and appropriately formatted port config
- Write Port Config writes it with added values

- Add SPI/Add GPIO adds rows to the respective tables

- Send Files sends sound files to the Pi server sounds folder.
- Test Run asks you to select motor config and anim data files which are then
streamed to the Pi server to be played.

Debug Tab:
setBlenderPath - set paths to blender.exe or bforartists.exe
setPiAddress - set host path to raspberry pi server. 
View animation data sent to local server at http://host:port/animate

TODO

- Wrap app as .exe (Windows), .dmg (Mac), and .elf (Linux), using pyinstaller lib.
    (also optional compatibility with FreeBSD, Solaris and AIX)
- Controller support for L6470 ST IC
- Basic 3D Printer integration, just repurpose the code on line 725 of roboanimator.py with
another button
- More error catching
- More menu options
- Add undo/redo, other editing features to make system more robust.
- Style style style
- Fix file select for non .blend files so you don't have to manually import
- Detach the blender process correctly for concurrent running. 
- Add table templates/buttons


PYQT5 INSTALLATION (temp for build)
 
- Install Anaconda Navigator

Once you have Anaconda installed:

- Install spyder on the Home tab
- Go the the Environments tab, click the play button on the base(root) environment and Open Terminal

- from the Terminal type in

`pip install PyQt5`

(optional for visual editor) 
After this completes type in

`pip install pyqt5-tools`

- Yes the case of those letters for the terminal commands are specific

- Once those are done navigate to C://Users/YOURUSERNAME/Anaconda3/Lib/site-packages/pyqt5-tools and open QtDesigner.

Alright and from there, as long as everything's installed correctly, 

- run the `roboanimator.py` file with spyder and the interface should show up. 

There is a debug command to link blender. Or you can set it yourself in the init file.
