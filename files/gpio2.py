from gpiozero import Button
from gpiozero.pins.rpigpio import RPiGPIOFactory
from signal import pause

# Specify the RPiGPIO pin factory
factory = RPiGPIOFactory()

# Initialize the Button with the specified pin factory
button = Button(16, pull_up=True, pin_factory=factory)

def on_button_pressed():
    print("Button Pressed")

def on_button_released():
    print("Button Released")

button.when_pressed = on_button_pressed
button.when_released = on_button_released

pause()

