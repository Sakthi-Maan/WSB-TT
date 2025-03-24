# import RPi.GPIO as GPIO
# import time

# # Define the GPIO pins using BCM numbering
# arr1 = [5, 6, 13, 19]  # Corresponds to Physical Pins 29, 31, 33, 35
# diff = 15

# def setup():
#     GPIO.setmode(GPIO.BCM)
#     for pin in arr1:
#         GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     time.sleep(0.5)

# def readSwitch():
#     total2 = 0  # Reset total to 0 for each read
#     if GPIO.input(arr1[0]) == GPIO.HIGH:
#         total2 += 1
#     if GPIO.input(arr1[1]) == GPIO.HIGH:
#         total2 += 2
#     if GPIO.input(arr1[2]) == GPIO.HIGH:
#         total2 += 4
#     if GPIO.input(arr1[3]) == GPIO.HIGH:
#         total2 += 8
#     return total2
#     #return abs(total2 - diff)

# def main():
#     setup()
#     try:
#         global count
#         count = 0
#         while True:
#             switch_value = readSwitch()
#             if switch_value is not None:
#                 print(f"Switch Value: {switch_value} and Count: {count}")
#             count += 1
#             time.sleep(0.5)  # Adjusted delay for stability
#     except KeyboardInterrupt:
#         GPIO.cleanup()

# if __name__ == "__main__":
#     main()


# import RPi.GPIO as GPIO
# import time

# # Define the GPIO pins using BCM numbering
# arr1 = [5, 6, 13, 19]  # Corresponds to Physical Pins 29, 31, 33, 35
# diff = 15

# def setup():
#     GPIO.setmode(GPIO.BCM)
#     for pin in arr1:
#         GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     time.sleep(0.5)

# def readSwitch():
#     total2 = 0  # Initialize total to 0 for each read
#     pin_states = []  # List to store pin states for debugging

#     # Debounce delay
#     time.sleep(0.05)

#     for i in range(len(arr1)):
#         pin_state = GPIO.input(arr1[i])  # Read the state of the pin
#         pin_states.append(pin_state)  # Store the state for debugging

#         # Check if the pin is HIGH
#         if pin_state == GPIO.HIGH:
#             total2 += 1 << i  # Increment the total based on the pin index

#     # Print the pin states for debugging
#     print(f"Pin States: {pin_states}, Total Value: {total2}")
#     return abs(total2 - diff)  # Return the calculated value

# def main():
#     setup()
#     try:
#         global count
#         count = 0
#         while True:
#             switch_value = readSwitch()  # Read the switch value
#             if switch_value is not None:
#                 print(f"Switch Value: {switch_value} and Count: {count}")
#             count += 1
#             time.sleep(0.5)  # Adjusted delay for stability
#     except KeyboardInterrupt:
#         GPIO.cleanup()

# if __name__ == "__main__":
#     main()


import RPi.GPIO as GPIO
import time

# Define the GPIO pins using BCM numbering
arr1 = [6, 13, 19, 26]  # Corresponds to Physical Pins 29, 31, 33, 35
diff = 15


def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in arr1:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time.sleep(0.5)


def readSwitch():
    total2 = 0  # Reset total to 0 for each read
    if GPIO.input(arr1[0]) == GPIO.HIGH:
        total2 += 1
    if GPIO.input(arr1[1]) == GPIO.HIGH:
        total2 += 2
    if GPIO.input(arr1[2]) == GPIO.HIGH:
        total2 += 4
    if GPIO.input(arr1[3]) == GPIO.HIGH:
        total2 += 8
    return total2
    # return abs(total2 - diff)


def main():
    setup()
    try:
        global count
        count = 0
        while True:
            switch_value = readSwitch()  # Read the switch value
            if switch_value is not None:
                print(f"Switch Value: {switch_value} and Count: {count}")
            count += 1
            time.sleep(0.5)  # Adjusted delay for stability
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
