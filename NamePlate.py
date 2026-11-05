"""
# NamePlate.py
# Controller coordinating Employees, LCDDisplay, Buttons, LightStrip, and PassiveBuzzer
"""
import time
from Log import *
from Lights import GREEN, YELLOW, RED

class NamePlate:
    TONE_NAV = 523    # C5
    TONE_AVAIL = 659  # E5

    def __init__(self, employees, display, buttons, lightstrip, buzzer):
        self.employees = list(employees)
        self._current_index = 0
        self._current_page = 0
        self._last_page_flip = time.ticks_ms()
        self.PAGE_INTERVAL_MS = 3000  # Automatically rotate details every 3 seconds

        self.display = display
        self.buttons = list(buttons)
        self.lightstrip = lightstrip
        self.buzzer = buzzer

        self.updateDisplay()

    def currentEmployee(self):
        return self.employees[self._current_index]

    def nextEmployee(self):
        self._current_index = (self._current_index + 1) % len(self.employees)
        self._current_page = 0
        self._last_page_flip = time.ticks_ms()
        if self.buzzer:
            self.buzzer.beep(self.TONE_NAV, 60)
        self.updateDisplay()

    def previousEmployee(self):
        self._current_index = (self._current_index - 1) % len(self.employees)
        self._current_page = 0
        self._last_page_flip = time.ticks_ms()
        if self.buzzer:
            self.buzzer.beep(self.TONE_NAV, 60)
        self.updateDisplay()

    def changeAvailability(self):
        self.currentEmployee().cycleAvailability()
        if self.buzzer:
            self.buzzer.beep(self.TONE_AVAIL, 80)
        self.updateDisplay()

    def tick(self):
        """Call inside the main loop to handle multi-page cycling"""
        now = time.ticks_ms()
        screens = self.currentEmployee().get_screens()
        if len(screens) > 1 and time.ticks_diff(now, self._last_page_flip) > self.PAGE_INTERVAL_MS:
            self._current_page = (self._current_page + 1) % len(screens)
            self._last_page_flip = now
            self.refresh_screen_text()

    def refresh_screen_text(self):
        screens = self.currentEmployee().get_screens()
        line0, line1 = screens[self._current_page % len(screens)]
        if self.display:
            self.display.clear()
            self.display.showText(line0[:16], 0, 0)
            self.display.showText(line1[:16], 1, 0)

    def updateDisplay(self):
        self.refresh_screen_text()
        
        # Update NeoPixel Lightstrip color based on availability
        if self.lightstrip:
            status = self.currentEmployee().getAvailability().lower()
            if status == "available":
                self.lightstrip.setColor(GREEN)
            elif status == "away":
                self.lightstrip.setColor(YELLOW)
            else:
                self.lightstrip.setColor(RED)

    def buttonPressed(self, name):
        norm = str(name).strip().lower()
        if "next" in norm:
            self.nextEmployee()
        elif "prev" in norm:
            self.previousEmployee()
        elif "avail" in norm:
            self.changeAvailability()