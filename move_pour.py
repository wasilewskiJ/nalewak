import requests, time, random
from vision_system.vision_system import vision_system


HOST = "localhost"
PORT = 7125
API_KEY = "56831fa1de8f4676a6be1b703c1bdf94"

max_x = 579
max_y = 544

def run_gcode(gcode):
    r = requests.post(f"http://{HOST}:{PORT}/printer/gcode/script?script={gcode}", headers={"X-Api-Key": API_KEY})
    return r.json()

def get_status():
    r = requests.get(f"http://{HOST}:{PORT}/server/info", headers={"X-Api-Key": API_KEY})
    return r.json()

def home():
    r = run_gcode("G28")
    return r.json()

def move(x, y):
    gcode = f"G0 X{min(x, max_x)} Y{min(y, max_y)} F10000"
    r = run_gcode(gcode)
    if 'error' in r and r['error'] != None and r['error']['code'] == 400 and r['error']['message'].startswith('Must home'):
        home()
        time.sleep(5)
        # TODO: Wykrywać jakoś czy już jest zahomowane zamiast time.sleep
        run_gcode(gcode)

if __name__ == "__main__":
	vision_system()

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


