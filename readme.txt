This program calculates the sun vector based on the sensor values of 12 LDR sensors,
placed on 6 sides of a cubesat representative structure. The LDR_readout.ino file can
be used to upload the code to the attitude determination board. The python program handles
reading out the serial port and determining the attitude.

[PYTHON MODULES]
Required modules:

- math
- configparser
- serial
- time

[CALIBRATION]
Calibration of each sensor should be performed before usage. The minimum values
of each sensor correspond to the darkness read-out. The maximum values correspond to the
values at 90° incidence angle, for the used light source, at the specific light source distance.
Calibration values can be adapted and saved in the 'calibration.ini' file.