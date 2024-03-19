# Autonomiczny Nalewak do Napojów #
# Autonomous Beverage Dispenser #

## About the project ##
The project of an autonomous beverage dispenser with a vision system based on Raspberry Pi is a robot that allows for automatic pouring of a specific amount of liquid (e.g. water, juice, etc.) into cups/glasses. It uses Arduino with stepper motors and Klipper3D to control the robot axes. Vision system is based on wide-angle camera with Raspberry Pi. The only other sensors used in the project apart from the camera are the end-switches used in the control system.
<video>

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
We were using push-button for sending start command to robot (web app is on todo list). The script **gpio_button.py** handles button service and starts robot by calling run() function from **move_pour.py** module. So if you want to constantly listen to button push in loop, use:
```
python gpio_button.py
```
If you placed cups, you can now push the button. Robot will take photo, scan it for cups, locate their coordinates and then move to cups and pour the beverage. **IT'S VERY IMPORTANT TO NOT CHANGE THE PLACEMENT OF CUPS AFTER PUSHING THE BUTTON** - robot uses taken photo in moment of button push to locate coordinates of cups. So if you will change the placement after button push, robot won't be able to target the cups.

If you would like to manually start the robot every time you place the cups, run the command below:
```
python move_pour.py
```

Robot must home it's axes every first start. When the robot is idle, it stays in it's max position (579, 544) mm - top right corner. If there will be Arduino shutdown - robot will run FIRMWARE_RESTART command in Klipper, then will home and then continue last interrupted process.


  
