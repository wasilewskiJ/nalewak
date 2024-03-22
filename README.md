# Autonomiczny Nalewak do Napojów #
# Autonomous Beverage Dispenser #

## About the project ##
The project of an autonomous beverage dispenser with a vision system based on Raspberry Pi is a robot that allows for automatic pouring of a specific amount of liquid (e.g. water, juice, etc.) into cups/glasses. It uses Arduino with stepper motors and Klipper3D to control the robot axes. Vision system is based on wide-angle camera with Raspberry Pi. The only other sensors used in the project apart from the camera are the endstops used in the control system.

![Autonomous beverage dispenser](https://lh3.googleusercontent.com/u/1/drive-viewer/AKGpihY4Ds88guXWTf6SJowu3OumF_aubBPPEXEGs7TINiyMgXItxIrY_UPugz1Nocb0jx5w-EFktZdDalxKAt3sy4ylCh8eCg=w1850-h968)

<link to project page/>

## Requirements ##
- Our robot - "nalewak" :)<br>
**TODO: Update requirements**

## Installation ## 
- Clone the repository to Raspberry with the following command:
  ```
  git clone https://github.com/wasilewskiJ/nalewakVisionSystem.git
  ```
- Next, create virtual environment and install dependencies:
  ```
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
  That's all.
  
## Usage ##
We were using push-button for sending start command to robot (web app is on todo list). The script `gpio_button.py` handles button service and starts robot by calling run() function from `move_pour.py` module. So if you want to constantly listen to button push in loop, use:
```
python gpio_button.py
```
If you placed cups, you can now push the button. Robot will take photo, scan it for cups, locate their coordinates and then move to cups and pour the beverage. **IT'S VERY IMPORTANT TO NOT CHANGE THE PLACEMENT OF CUPS AFTER PUSHING THE BUTTON** - robot uses taken photo in moment of button push to locate coordinates of cups. So if you will change the placement after button push, robot won't be able to target the cups.

If you would like to manually start the robot every time you place the cups, run the command below:
```
python move_pour.py
```

### Background service ###
There is a background systemctl service called **gpio_button.service** configured to run automaticaly on boot on the RPi. It works like `gpio_button.py` but all the time in background.
Here are some example commands to manage the service:

Restarting the service (for example after changing the code):
```
sudo systemctl restart gpio_button
```
‌
Check the status:
```
sudo systemctl status gpio_button
```

Stop the service:
```
sudo systemctl stop gpio_button
```

Run the service:
```bash
sudo systemctl start gpio_button
```

Show logs:
```bash
sudo journalctl -u gpio_button --no-pager
```

Robot must home it's axes every first start. When the robot is idle, it stays in it's max position (579, 544) [mm] - top right corner. If an Arduino shutdown happens - robot will run FIRMWARE_RESTART command in Klipper, then will home and then continue last interrupted process. 

In the current configuration, robot takes image, scans for cups, locate their coordinates and starts moving and pouring. It always goes to closest cup, pour the beverage (actually for 5.5 seconds), then it shakes to remove beverage drops, waits for 2 seconds, and goes to the next closest cup. In this way it handles all the cups and returns to the MAX position.

**If anything goes wrong, there is an emergency button on the top edge of box with power supply** - it will turn off the motors and the pump. Currently, there is a separate power supply circuit for microcontrollers, so they will remain turned on, but we plan to change this in the future. If you will release the emergency button, the program will continue from the moment it was interrupted. So we recommend to disable raspberry plug-in.

The pouring area of "nalewak" in current camera position is specified in `vertices.txt`. There are listed pixel coordinates of pouring area vertices in the following order: top-left, top-right, bottom-right, bottom-left. If you will change camera position/pouring area, then you need to take a new photo with cups in the corners of the area, and put them inside `vertices.txt` in order as mentioned earlier.   

## Contents overview ## 
- **vision_system/** - vision_system module
  - `vision_system.py` - runs all vision_system submodules
  - `take_photo.py` - takes photo from camera in 1920x1080, using openCV
  - **correct/** - submodule for removing fisheye distortions and cropping the image to the appropriate format
    - `correct.py` - removes fisheye distortion from the image by using a pre-calculated matrix saved in `dist_pickle.p`
    - `crop.py` - crops the image to leave only the pouring area
  - **network/** - submodule with neural network used to detect cups in an image
    - `model/` - TensorFlowLite model trained for cup detecting
    - `detect_mug.py` - detects mugs/cups and labels them with green rectangle. Then finds bottom centers of found cups and checks if they are in the pouring area. Rejects point outside of the area. Saves coordinates of centers in `../plan_view/centers.pkl`
  - **results/** - also saved results from detect_mug.py.
    - `ready_img.txt` - all detections, including rejected, save line by line, in format: [label] [certainty] [left-top corner of object] [right-bottom corner of object]
    - `ready_img.png` - image with labeled detected objects
  - **plan_view/** -  submodule for transforming image to overhead view of the pouring area
    - `centers.pkl` - saved centers of cups detected by `../network/detect_mug.py`
    - `vertices.txt` - coordinates of pouring area vertices, used in `plan_view.py` module
    - `transform.py` - submodule used in `plan_view.py`. It computes width and height of "plan view" image and calculates transform matrix, which the submodule returns.
    - `plan_view.py` - passes vertices to `transform.py` in order to get transform matrix and applies that matrix to cup centers saved in `centers.pkl`. Then it scales centers coordinates to robot dimensions, prints them and returns as a result. You can specify the OUTPUT flag in function parameters, it will save the plan view result image.
- `move_pour.py` - handles communication with Klipper via API SERVER, starts the vision_system and runs all Klipper commands in order to move and pour a beverage.
- `gpio_button.py` - listens for button push, and if pushed, starts a thread running `move_pour.py` module
- **system/** - directory containing system configurations
  - `printer.cfg` - Klipper configuration
  - `gpio_button.service` - service that you can start via systemctl command. It listens to the button push in background and runs the robot if pushed.

## Hardware ##
- Raspberry Pi 4B
- Wide-angle camera for Raspberry Pi, OV5647 5Mpx Waveshare
- 3x stepper motor NEMA17 17HS4401
- 3x motor driver TB6600
- 3x endstop switch
- Diaphragm pump 6-12V DC R385, WATER-AIR
- 5V 10A relay
## Software ##
- Klipper3D
- TensorFlow SSD-Mobilenet-V2-FPNlite-320 model 
