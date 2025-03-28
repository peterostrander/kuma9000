import gpiod
import time
import os

print("Available GPIO chip:")

for i in range(4):
    try:
        chip = gpiod.Chip(f"gpiochip{i}")
        print(f"- Found: gpiochip{i}")
    except OSError:
        continue

LED_PIN = 14
POWER_BUTTON_PIN = 3
RESET_BUTTON_PIN = 2

chip = gpiod.Chip("gpiochip0")
led = chip.get_line(LED_PINT)
power_button = chip.get_line(POWER_BUTTON_PIN)
reset_button = chip.get_line(RESET_BUTTON_PIN)

led.request(consumer="kuma-led", type=gpiod.LINE_REQ_DIR_OUT)
power_button.request(consumer="kuma-power", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
reset_button.request(consumer="kuma-reset", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

# Blnk LED to indicate service is running
for _ in range(3):
    led.set_value(1)
    time.sleep(0.2)
    led_set_value(0)
    time.sleep(0.2)
led.set_value(1)

print("Kuma controller running...")

while True:
    if power_button.event_wait(timeout=1):
        event = power_button.event_read()
        if event.type == gpiod.LineEvent.FALLING_EDGE:
            print("Power button pressed. Shutting down...")
            os.system("shutdown now")

    if reset_button.event_wait(timeout=0.1):
        event = reset_button.event_read()
        if event.type == gpiod.LineEvent.FALLING_EDGE:
            print("Reset button pressed. Rebooting...")
            os.system("reboot")
