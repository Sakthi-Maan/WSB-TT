import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BOARD)  # Use BOARD pin numbering

# Define the GPIO pins for the wheel switch
WHEEL_SWITCH_PINS = [6, 13, 19, 26]

# Set up the GPIO pins as inputs
for pin in WHEEL_SWITCH_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# List to store the detected sequence (up to 10 values)
detected_sequence = []


def read_wheel_switch():
    value = 0

    # Read the values from the GPIO pins
    for i, pin in enumerate(WHEEL_SWITCH_PINS):
        input_value = GPIO.input(pin)
        # If the pin reads LOW, set the corresponding bit in the value
        if input_value == GPIO.LOW:
            value += 1 << i  # Set the bit at position i

    return value


try:
    while True:
        # Read the wheel switch value
        value = read_wheel_switch()

        # Store the value if it's not already in the sequence and within the range 0-9
        if value not in detected_sequence and 0 <= value < 10:
            detected_sequence.append(value)

        # Print the current wheel switch value
        print(f"Current Wheel Switch Value: {value}")

        # Print the detected sequence (up to 10 values)
        if len(detected_sequence) > 0:
            print(f"Detected Sequence: {detected_sequence}")

        # Stop reading after capturing the first 10 unique values
        if len(detected_sequence) >= 10:
            print("Captured the first 10 values. Stopping.")
            break

        # Delay for a short period to avoid excessive printing
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Clean up GPIO settings
