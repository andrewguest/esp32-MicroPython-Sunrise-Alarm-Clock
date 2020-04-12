from time import sleep_ms, sleep
from machine import Pin
from neopixel import NeoPixel
import urequests
import ujson


time_api_url = "http://worldclockapi.com/api/json/cst/now"
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

np = NeoPixel(Pin(26), 19)
n = np.n


# Turns on all of the NeoPixels in a fading pattern.
# The brightness of each led (Red, Green, and Blue) are increased
#   by 20 every 5 seconds until they reach a max value of (200, 200, 200)
# Then the NeoPixels stay at that brightness and color (white) for 30 seconds
#   when clear_leds() is called before running alternate_leds()
def fade_brightness_up():
    print("fade_brightness_up")
    brightness = 0
    while brightness <= 200:
        brightness += 20
        for led in range(n):
            np[led] = (brightness, brightness, brightness)
        sleep(5)
        np.write()
    sleep(30)
    clear_leds()
    alternate_leds()


# Turns on all of the even numbered NeoPixels for 250 milliseconds
#   then turns them off and turns on the odd numbered Neopixels
#     for 250 milliseconds.
# This pattern is repeated 50 times and then all of the
#   Neopixels are turned off with the clear_leds() function.
# Then the entire process starts over again by calling check_time()
def alternate_leds():
    print("alternate_leds")
    for i in range(50):
        for j in range(n):
            if (j % 2) == 0:
                np[j] = (0, 0, 0)
            else:
                np[j] = (240, 240, 240)
        np.write()
        sleep_ms(250)
        for j in range(n):
            if (j % 2) == 0:
                np[j] = (240, 240, 240)
            else:
                np[j] = (0, 0, 0)
        np.write()
        sleep_ms(250)
    sleep(60)
    clear_leds()
    check_time()


# Turns all of the NeoPixels off
def clear_leds():
    print("clear_leds")
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


# Check if it's a weekday and, if it is, then check if
#   the current time is between 6:00am and 6:10am
def check_time():
    clear_leds()
    print("check_time")
    data = urequests.get(time_api_url)
    data = ujson.loads(data.text)

    day_of_the_week = data["dayOfTheWeek"]

    current_time = data["currentDateTime"]
    current_time = current_time.split("T")[1]
    current_time = current_time.split("-")[0]
    hour = int(current_time.split(":")[0])
    minutes = int(current_time.split(":")[1])

    # If it's Monday, Tuesday, Wednesday, Thursday, or Friday then proceed on to the hour and minute checks
    #   otherwise, sleep for 4 hours
    if day_of_the_week in weekdays:
        if hour == 6 and 0 <= minutes <= 10:
            fade_brightness_up()
        # If the current time is after 6am, then sleep for 4 hours
        elif hour > 6:
            sleep(14400)
        else:
            # sleep 5 minutes
            sleep(300)
    else:
        # sleep 4 hours
        sleep(14400)


if __name__ == "__main__":
    while True:
        check_time()
