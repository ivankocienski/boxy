# Boxy

A thing for drawing simple box like worlds

## Requirements

- python >3
- pygame
- pyopengl


## Usage

Run `python Boxy.py` and it boots up into 2D mode. It will try to load map.txt and put you in the home location.

In this mode
- move player around with cursor keys
- change player position by pressing `home` key
- select a box (room) with the left mouse button
  - you can then delete the box
- start plotting new boxes by positioning the mouse cursor and pressing `spacebar` once.
  - then move the mouse to size up your room and press `spacebar` again.
  - rooms can only be drawn in the positive X/Y direction
  - rooms cannot overlap
  - rooms that touch each other will automatically join
- Q quits the program immediatly
- F2 saves to map.txt

Press enter to switch to 3D mode
- move about with the cursor keys
- pressing C cycles the current room you are in to the next color

