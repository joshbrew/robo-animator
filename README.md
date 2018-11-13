# Robo-Animator
Test UI


HOW TO USE
- With PyQt5 on the machine running the app and Flask on the Pi installed.

- Run Testrun_server.py on the Pi
- Run roboanimator.py on the client machine

Buttons
- Edit & Import Animation opens blender with a selected .blend file, or none at all for a
blank animation. When you close this instance of blender, the app unfreezes and imports any
armiture data available in that animation.
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


EASY INSTALLATION (temp for build)

- Install Anaconda Navigator

Once you have Anaconda installed:

- Install spyder on the Home tab
- Go the the Environments tab, click the play button on the base(root) environment and Open Terminal

- from the Terminal type in


pip install PyQt5


(optional for visual editor) 
After this completes type in


pip install pyqt5-tools


- Yes the case of those letters for the terminal commands are specific


- Once those are done navigate to C://Users/YOURUSERNAME/Anaconda3/Lib/site-packages/pyqt5-tools and open QtDesigner.

Alright and from there, as long as everything's installed correctly, 

- run the roboanimator.py file with spyder and the interface should show up. 

There is a debug command to link blender. Or you can set it yourself in the init file.
