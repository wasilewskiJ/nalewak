import requests, time, random
from vision_system.vision_system import vision_system
import subprocess
from math import dist
import numpy as np

HOST = "localhost"
PORT = 7125
API_KEY = "56831fa1de8f4676a6be1b703c1bdf94"

max_x = 579
max_y = 544
F = 13000
CLEANING_F = 80000
POUR_TIME = 5.5 #seconds

emergency_stop = False

def run_gcode(gcode):
    try:
        r = requests.post(f"http://{HOST}:{PORT}/printer/gcode/script?script={gcode}", headers={"X-Api-Key": API_KEY}, timeout=20)
    except requests.exceptions.ConnectionError:
        print("ConnectionError. Trying FIRMWARE_RESTART")
        subprocess.Popen("echo 'FIRMWARE_RESTART' > /tmp/printer", shell=True)
        time.sleep(5)
        home() #must home after FIRMWARE RESTART
        return run_gcode(gcode)
    
    r = r.json()

    if 'error' in r and r['error'] != None and r['error']['code'] == 400 and r['error']['message'].startswith('Must home'):
        print("Must home")
        home()
        print("Homed")
        return run_gcode(gcode)
    
    elif 'error' in r and r['error'] != None and not r['error']['message'].startswith('Must home'):
        print(r['error'])

    return r

def get_status():
    r = requests.get(f"http://{HOST}:{PORT}/server/info", headers={"X-Api-Key": API_KEY})
    return r.json()

def stop():
    global emergency_stop
    emergency_stop = True

#wait until robot is accesible
def wait():
    r = run_gcode("M400")
    return r

def set_acceleration(value):
    r = run_gcode(f"M204 S{value}")
    return r

def set_absolute_cords():
    r = run_gcode("G90")
    return r

def set_relative_cords():
    r = run_gcode("G91")
    return r

def home():
    set_acceleration(200)
    wait()
    r = run_gcode(f"G28 X Y F{F}")
    wait()
    return r

def move_to_points(pts):
    current_position = (max_x, max_y)
    
    while pts:
        # Calculating the distance from the current position to each point
        distances = [dist(current_position, pt) for pt in pts]
        
        # Finding the index of the closest point
        closest_point_index = np.argmin(distances)
        print(f'Going to closest point: {pts[closest_point_index]}')
        
        # Moving and pouring to the closest point
        move_pour([pts[closest_point_index]])
        
        # Updating the current position
        current_position = pts[closest_point_index]
        
        # Removing the point we have just approached
        del pts[closest_point_index]
    max()

def max():
   r = run_gcode(f"G0 X579 Y544 F{F}")
   return r

def clean(iterations=10, log=True):
    if log:
        print('Cleaning')
    set_relative_cords()
    wait()
    set_acceleration(2000)
    wait()
    for i in range(iterations):
        if i % 2 == 0:
            run_gcode(f'G0 X-10 Y-10 F{CLEANING_F}')
        else:
            run_gcode(f'G0 X10 Y10 F{CLEANING_F}')
    set_absolute_cords()
    wait()
    set_acceleration(200)
    wait()
    time.sleep(2)

def move_pour(pt):
    gcode = f"G0 X{min(pt[0][0], max_x)} Y{min(pt[0][1], max_y)} F{F}"

    print("Going to cup")
    run_gcode(gcode)

    print("Waiting")
    wait()
    
    print("Pouring")
    run_gcode(f"POUR TIME={POUR_TIME}")
    wait()
    
    clean() 


def run():
    set_acceleration(200)
    wait()
    center_of_mug = vision_system()
    move_to_points(center_of_mug)

if __name__ == "__main__":
    run()
