print("...\033[F")

import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from time import sleep
import threading
import termios
import sys

def print_waffle_state():
    global waffle_counter
    global last_waffle_at
    global last_waffle_at

    time_delta = (datetime.now() - first_waffle_at)
    minutes = (time_delta.seconds + time_delta.microseconds / 1000000) / 60
    wpm = waffle_counter / minutes
    print("Waffle Number: {0:5}  -  {1:6.2f} WPM       \033[F".format(waffle_counter, wpm))
    with open("waffle_count.txt", "a") as myfile:
        myfile.write("{}: {}\n".format(last_waffle_at, waffle_counter))
def handle_admin_commands():
    global waffle_counter
    global first_waffle_at
    try:
        command = sys.stdin.read(1)
        if command == "h": # arrow up
            waffle_counter += 1
        elif command == "r": # arrow down
            waffle_counter -= 1
        elif command == "f": # arrow down
            first_waffle_at = datetime.now()
        print_waffle_state()
    except IOError:
        pass

old_term_state = termios.tcgetattr(sys.stdin.fileno())
term_state = termios.tcgetattr(sys.stdin.fileno())
term_state[3] &= ~termios.ECHO & ~termios.ICANON
termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, term_state)


waffle_iron_detector_pin = 40

waffle_iron_open = True
waffle_counter = 0
first_waffle_at = datetime.min
last_waffle_at = datetime.min
waffle_cooloff = timedelta(seconds=3)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(waffle_iron_detector_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("All setup!")
print("No Waffles yet :(\033[F")
while True:
    handle_admin_commands()
    GPIO.wait_for_edge(waffle_iron_detector_pin, GPIO.FALLING, timeout=200)
    if GPIO.input(waffle_iron_detector_pin) == GPIO.LOW:
        waffle_iron_open = False
        continue
    if waffle_iron_open:
        continue
    waffle_iron_open = True
    if last_waffle_at + waffle_cooloff >= datetime.now():
        continue
    if first_waffle_at == datetime.min:
        first_waffle_at = datetime.now()
    last_waffle_at = datetime.now()

    waffle_counter += 1
    print_waffle_state()
    sleep(0.2)

