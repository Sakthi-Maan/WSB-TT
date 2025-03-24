import RPi.GPIO as GPIO
import time

# Define the GPIO pins using BCM numbering
arr1 = [6, 13, 19, 26]   # Corresponds to Physical Pins 29, 31, 33, 35
arr2 = [12, 16, 20, 21]
arr3 = [24, 25, 8, 7]
arr4 = [4, 17, 27, 22]

diff = 15


def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in arr1 + arr2 + arr3 + arr4:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time.sleep(0.5)


def readSwitch():
    total1 = 0
    total2 = 0  # Reset total to 0 for each read
    total3 = 0
    total4 = 0
    if GPIO.input(arr1[0]) == GPIO.HIGH:
        total2 += 1
    if GPIO.input(arr1[1]) == GPIO.HIGH:
        total2 += 2
    if GPIO.input(arr1[2]) == GPIO.HIGH:
        total2 += 4
    if GPIO.input(arr1[3]) == GPIO.HIGH:
        total2 += 8
    "-----------------------------"
    if GPIO.input(arr2[0]) == GPIO.HIGH:
        total1 += 1
    if GPIO.input(arr2[1]) == GPIO.HIGH:
        total1 += 2
    if GPIO.input(arr2[2]) == GPIO.HIGH:
        total1 += 4
    if GPIO.input(arr2[3]) == GPIO.HIGH:
        total1 += 8
    "-----------------------------"
    if GPIO.input(arr3[0]) == GPIO.HIGH:
        total3 += 1
    if GPIO.input(arr3[1]) == GPIO.HIGH:
        total3 += 2
    if GPIO.input(arr3[2]) == GPIO.HIGH:
        total3 += 4
    if GPIO.input(arr3[3]) == GPIO.HIGH:
        total3 += 8

    "-----------------------------"
    if GPIO.input(arr4[0]) == GPIO.HIGH:
        total4 += 1
    if GPIO.input(arr4[1]) == GPIO.HIGH:
        total4 += 2
    if GPIO.input(arr4[2]) == GPIO.HIGH:
        total4 += 4
    if GPIO.input(arr4[3]) == GPIO.HIGH:
        total4 += 8
    # return total2
    return str(abs(total2 - diff))+str(abs(total1 - diff))+str(abs(total3 - diff))+str(abs(total4 - diff))


def main():
    setup()
    try:
        global count
        count = 0
        while True:
            switch_value = readSwitch()
            if switch_value is not None:
                print(f"Switch Value: {switch_value} and Count: {count}")
            count += 1
            time.sleep(0.5)  # Adjusted delay for stability
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
