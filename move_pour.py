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
POUR_TIME = 5.5 #sekundy

emergency_stop = False

def run_gcode(gcode):
    try:
        r = requests.post(f"http://{HOST}:{PORT}/printer/gcode/script?script={gcode}", headers={"X-Api-Key": API_KEY}, timeout=20)
    except requests.exceptions.ConnectionError:
        print("ConnectionError. Trying FIRMWARE_RESTART")
        subprocess.Popen("echo 'FIRMWARE_RESTART' > /tmp/printer", shell=True)
        time.sleep(5)
        home()
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
 
def wait():
    r = run_gcode("M400")
    return r

#def get_position():
#    run_gcode("M114")
#    time.sleep(1)
#    r = requests.get(f"http://{HOST}:{PORT}/printer/objects/query?objects=virtual_sdcard,print_stats,display_status", headers={"X-Api-Key": API_KEY})
#    return r

def home():
    run_gcode("M204 S200")
    wait()
    r = run_gcode(f"G28 X Y F{F}")
    wait()
    return r

def move_to_points(pts):
    current_position = (579, 544)
    
    while pts:
        # Obliczanie odległości od bieżącej pozycji do każdego punktu
        distances = [dist(current_position, pt) for pt in pts]
        
        # Znajdowanie indeksu najbliższego punktu
        closest_point_index = np.argmin(distances)
        print(f'Jade do najblizszego punktu: {pts[closest_point_index]}')
        
        # Przeniesienie do najbliższego punktu
        move([pts[closest_point_index]])
        
        # Aktualizacja bieżącej pozycji
        current_position = pts[closest_point_index]
        
        # Usunięcie punktu, do którego właśnie podjechaliśmy
        del pts[closest_point_index]
    max()

def max():
   r = run_gcode(f"G0 X579 Y544 F{F}")
   return r

def clean(iterations=10, log=True):
    if log:
        print('Cleaning')
    run_gcode("G91")
    wait()
    run_gcode("M204 S2000")
    wait()
    for i in range(iterations):
        if i % 2 == 0:
            run_gcode(f'G0 X-10 Y-10 F{CLEANING_F}')
        else:
            run_gcode(f'G0 X10 Y10 F{CLEANING_F}')
    run_gcode("G90")
    wait()
    run_gcode("M204 S200")
    wait()
    time.sleep(2)

def move(pt):
    gcode = f"G0 X{min(pt[0][0], max_x)} Y{min(pt[0][1], max_y)} F{F}"
    # gcode = f"MOVE_POUR X={round(min(pt[0][0], max_x))} Y={round(min(pt[0][1], max_y))} TIME=1"

    print("Going to cup")
    run_gcode(gcode)

    print("Waiting")
    wait()
    
    print("Pouring")
    run_gcode(f"POUR TIME={POUR_TIME}")
    wait()
    
    clean() 


def run():
    run_gcode("M204 S200")
    wait()
    center_of_mug = vision_system()
    move_to_points(center_of_mug)

if __name__ == "__main__":
    run()


# while True:
#     run_gcode("ARM_OPEN")
#     time.sleep(.2)
#     run_gcode("ARM_CLOSE")
#     time.sleep(.2)


# connect to websocket
#  ws://host_or_ip:port/websocket


# with connect(f"ws://{HOST}:{PORT}/websocket") as websocket:
#     print("Connected to websocket")
#     # send a message
#     websocket.send('{"jsonrpc": "2.0", "method": "server.info", "id": 1, "params": {"api_key": "56831fa1de8f4676a6be1b703c1bdf94"}}')
#     # receive a message
#     response = websocket.recv()
#     print(response)
#     # close the connection
#     websocket.close()
#     print("Connection closed")

# import socket

# server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
# server.bind("/tmp/klippy_uds")
# # server.listen(1)
# conn, addr = server.accept()

# print(f"Connection from {addr} has been established")

# conn.send('{ "jsonrpc": "2.0", "method": "server.info", "id": 1 }'.encode())


