import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO 16 as an input with an internal pull-up resistor
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Read the state of GPIO 16
        button_state = GPIO.input(16)
        if button_state == GPIO.LOW:
            print("Button Pressed")
        else:
            print("Button Released")
        time.sleep(0.1)  # Add a small delay to debounce
except KeyboardInterrupt:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()

