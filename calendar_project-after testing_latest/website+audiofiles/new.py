import RPi.GPIO as GPIO
import time

arr1 = [6, 13, 19, 26]
arr2 = [12, 16, 20, 21]
arr3 = [24, 25, 8, 7]
arr4 = [4, 17, 27, 22]

diff = 15


def setup_pins():
    """Sets up GPIO pins as inputs with pull-up resistors."""
    GPIO.setmode(GPIO.BCM)
    for pin in arr1 + arr2 + arr3 + arr4:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time.sleep(0.5)  # Ensure all pins are properly set up


def read_array(arr):
    """Reads the GPIO input values for a given array of pins and calculates the total."""
    total = 0
    for i, pin in enumerate(arr):
        if GPIO.input(pin) == GPIO.HIGH:
            total += 2**i
    return total


def read_switches():
    """Reads all switch arrays and returns the calculated string based on the 'diff' value."""
    total1 = read_array(arr1)
    total2 = read_array(arr2)
    total3 = read_array(arr3)
    total4 = read_array(arr4)

    # return f"{abs(total1 - diff)}"

    return f"{abs(total1 - diff)}{abs(total2 - diff)}{abs(total3 - diff)}{abs(total4 - diff)}"


def main():
    setup_pins()
    count = 0
    try:
        while True:
            switch_value = read_switches()
            print(f"Switch Value: {switch_value} and Count: {count}")
            count += 1
            time.sleep(0.5)  # Adjusted delay for stability
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("GPIO cleanup complete.")


if __name__ == "__main__":
    main()
