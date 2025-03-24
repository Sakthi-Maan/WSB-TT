import RPi.GPIO as GPIO
import time

# Define the GPIO pins connected to the BCD outputs
BCD_PINS = [6, 13, 19, 26]

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
for pin in BCD_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def read_bcd():
    value = 0
    for i, pin in enumerate(BCD_PINS):
        if GPIO.input(pin) == GPIO.HIGH:
            value += 1 << i
    return value


try:
    while True:
        bcd_value = read_bcd()
        print(f"BCD Value: {bcd_value}yes")
        time.sleep(0.5)  # Adjust the delay as needed
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    GPIO.cleanup()
