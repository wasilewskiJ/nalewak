# If you have RuntimeError: Not running on a RPi!
# Run the following commands:
# sudo chown root:$USER /dev/gpiomem
# sudo chmod g+rw /dev/gpiomem

from gpiozero import Buzzer
from time import sleep

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import move_pour
import threading

running = False
buzzer = Buzzer(17)

def buzzer_on(lenght=0.3,delay=0):
    sleep(delay)
    buzzer.on()
    sleep(lenght)
    buzzer.off()

def button_callback(channel=None):
    global running
    if running:
        print("Button was pushed, but already running!")
        return
    
    running = True
    print("Button was pushed!")

    buzzer_therad = threading.Thread(target=buzzer_on, args=(0.3,0.1))
    t1 = threading.Thread(target=move_pour.run)

    buzzer_therad.start()
    buzzer_therad.join()

    t1.start()
    t1.join()

    running = False

if __name__ == "__main__":
    move_pour.home()
    move_pour.max()
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled hight (on)

    # GPIO.add_event_detect(4,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

    # message = input("Listning for button press. Press enter to quit\n\n") # Run until someone presses enter

    buzzer_on(0.2)
    sleep(0.2)
    buzzer_on(0.2)

    # move_pour.max()

    print("Listning for button press. Ctrl+C to quit\n\n")
    while True:
        if GPIO.input(4) == GPIO.HIGH:
            button_callback()
    GPIO.cleanup() # Clean up

