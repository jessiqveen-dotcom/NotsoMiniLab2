"""
# main.py
# Main loop executing non-blocking button polling and display cycling
"""
import time
from Log import *
from Displays import LCDDisplay
from Button import Button
from LightStrip import LightStrip
from Buzzer import PassiveBuzzer
from Employee import Faculty, Staff, Administrator, StudentWorker
from NamePlate import NamePlate

if __name__ == "__main__":
    Log.i("Starting NamePlate Application...")

    # 1. Define people with required attributes
    people = [
        Faculty(
            name="Dr. Smith", 
            phone="305-348-0001", 
            position="Assoc Prof", 
            courses=["ISM6106", "ISM6316"], 
            office_hours="M/W 2-4PM",
            available="Available"
        ),
        Staff(
            name="John Davis", 
            phone="305-348-0002", 
            position="Adviser", 
            department="Grad Studies",
            available="Away"
        ),
        Administrator(
            name="Dr. White", 
            phone="305-348-0003", 
            position="Dean", 
            current_meeting="Board Review",
            available="Busy"
        ),
        StudentWorker(
            name="Alex Rivera", 
            phone="305-348-0004", 
            position="Assistant", 
            supervisor="Dr. Smith", 
            max_hours=20,
            available="Available"
        )
    ]

    # 2. Hardware components
    display = LCDDisplay(sda=0, scl=1)
    lightstrip = LightStrip(pin=2, name="StatusRing", numleds=8, brightness=0.5)
    buzzer = PassiveBuzzer(pin=16, name="Buzzer")

    # 3. Three individual push buttons
    btn_prev = Button(18, "Previous", lowActive=True)
    btn_next = Button(19, "Next", lowActive=True)
    btn_avail = Button(20, "Availability", lowActive=True)
    buttons = [btn_prev, btn_next, btn_avail]

    # 4. Controller
    nameplate = NamePlate(
        employees=people,
        display=display,
        buttons=buttons,
        lightstrip=lightstrip,
        buzzer=buzzer
    )

    last_press = 0
    DEBOUNCE_MS = 300

    Log.i("System Ready. Use buttons to navigate.")

    try:
        while True:
            now = time.ticks_ms()

            # Previous button check
            if btn_prev.isPressed():
                if time.ticks_diff(now, last_press) > DEBOUNCE_MS:
                    nameplate.previousEmployee()
                    last_press = now

            # Next button check
            if btn_next.isPressed():
                if time.ticks_diff(now, last_press) > DEBOUNCE_MS:
                    nameplate.nextEmployee()
                    last_press = now

            # Availability button check
            if btn_avail.isPressed():
                if time.ticks_diff(now, last_press) > DEBOUNCE_MS:
                    nameplate.changeAvailability()
                    last_press = now

            # Background update for flipping multi-screen text
            nameplate.tick()
            time.sleep_ms(30)

    except KeyboardInterrupt:
        display.clear()
        lightstrip.off()
        buzzer.stop()
        