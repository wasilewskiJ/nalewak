# SOFTWARE #

### KLIPPER CONFIGURATION ###

LOCATED ON RPi: /home/nalewak/printer.cfg
OR ACCESS VIA OCTOPRINT SERVER

Basic configuration like max positions, arduino PIN's, serial port to arduino, macros etc..


### NETWORK CONFIGURATION ###

The RPi addres is set to: 192.168.0.201

It creates it's own WiFi hotspot with these credentials:
ssid: nalewak_hotspot
pass: alarmpozarowy123!

In order to connect to RPi directly, you can use either a ssh or octoPrint server typing ip in web browser.

If you will to change network configuration, you can plug in SD card of RPi to PC, and edit wpa_supplicant.txt.
Detailed instruction:
https://rsw.io/how-to-setup-octoprint-octopi-to-work-on-wi-fi/ 


### HOW TO SEND G-CODES ###
Use either:
1. OctoPrint server in web browser
2. Send commands via terminal: echo [COMMAND] > /tmp/printer
3. Send commands via API SERVER 

AVAILABLE MACROS (type without [] brackets):


CALIBRATE - HOME AXIS AND RIDE TO MAX POSITION
 
MAX - GO TO MAX POSITION

MOVE_POUR X[POINT] Y[POINT] TIME[TIME_TO_POUR_SECONDS] - MOVE TO GIVEN POSITION AND POUR DRINK BY GIVEN TIME

POUR TIME[TIME_TO_POUR_SECONDS] - POUR DRINK BY GIVEN TIME

ARM_OPEN - Opens the robot's grip.

ARM_CLOSE - Closes the robot's grip.

ARM_UP - Raises the robot's arm to the highest position.

ARM_MIDDLE - Sets the robot's arm to the middle position.

ARM_LEVEL_2 - Positions the robot's arm to the second level height.

ARM_DOWN - Lowers the robot's arm to the lowest position.

ARM_0 - Rotates the robot's arm to 0 degrees.

ARM_45 - Rotates the robot's arm to 45 degrees.

ARM_90 - Rotates the robot's arm to 90 degrees.

ARM_135 - Rotates the robot's arm to 135 degrees.

ARM_180 - Rotates the robot's arm to 180 degrees.

*** CHECK OTHER MACROS IN printer.cfg ***

### SCRIPTS AND THEIR FUNCTIONALITY ###

*** vision_system/main.py *** - starts vision system job. Runs all subscripts

*** ./take_photo.py *** - takes photo in 1920x1080 resolution. Saves as _img.png_

*** correct/correct.py *** - uses _dist_pickle.p_ to defish a fisheye effect. Saves results as *corrected_img.png* 

*** correct/crop.py *** - crops *corrected_img.png* to desired size and saves as *ready_img.png*

*** network/model *** - directory that contains trained tensorflow model

*** network/detect_mug.py *** - detects mugs in *ready_img.png*. Finds centers of detected mugs and saves coordinates to *./list.p*

*** plan_view/transform.py *** - contains helper functions for projection.py

*** plan_view/projection.py *** - does plan view transformation and calculates centers of mugs. Corrects calculations using *correction_formulas.txt* and saves coordinates of mugs centers to *centers.txt*

*** ./send_commands.py *** - sends commands to Klipper via API Server using moonraker. Uses *plan_view/centers.txt*
