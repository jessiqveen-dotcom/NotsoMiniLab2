"""
# Employee.py
# Object-oriented inheritance hierarchy for digital nameplate employees
"""
from Log import *

class Employee:
    """Base class for all office members"""
    STATUSES = ("Available", "Away", "Busy")

    def __init__(self, name, phone, position, available="Available"):
        self.name = str(name)
        self.phone = str(phone)
        self.position = str(position)
        self.available = str(available)

    def getAvailability(self):
        return self.available

    def setAvailability(self, status):
        self.available = str(status)

    def cycleAvailability(self):
        try:
            idx = self.STATUSES.index(self.available)
            next_idx = (idx + 1) % len(self.STATUSES)
        except ValueError:
            next_idx = 0
        self.setAvailability(self.STATUSES[next_idx])
        return self.available

    def get_screens(self):
        """Returns a list of (line0, line1) tuples for the 16x2 LCD"""
        avail_tag = f"[{self.available[:4]}]"
        line0 = f"{self.name[:10]} {avail_tag:>5}"
        line1 = f"{self.position[:16]:<16}"
        screen2_line0 = f"Ph: {self.phone[:12]:<12}"
        screen2_line1 = f"Status: {self.available[:8]:<8}"
        return [(line0, line1), (screen2_line0, screen2_line1)]


class Faculty(Employee):
    """Faculty subtype displaying courses and office hours"""
    def __init__(self, name, phone, position, courses, office_hours, available="Available"):
        super().__init__(name, phone, position, available)
        self.courses = list(courses)
        self.office_hours = str(office_hours)

    def get_screens(self):
        avail_tag = f"[{self.available[:4]}]"
        # Screen 1: Name, status tag, and position
        s1_l0 = f"{self.name[:10]} {avail_tag:>5}"
        s1_l1 = f"{self.position[:16]:<16}"
        
        # Screen 2: Courses and phone number
        course_str = ",".join(self.courses)
        s2_l0 = f"Crs: {course_str[:11]:<11}"
        s2_l1 = f"Ph: {self.phone[:12]:<12}"
        
        # Screen 3: Office hours
        s3_l0 = "Office Hours:"
        s3_l1 = f"{self.office_hours[:16]:<16}"
        
        return [(s1_l0, s1_l1), (s2_l0, s2_l1), (s3_l0, s3_l1)]


class Staff(Employee):
    """Staff member with department information"""
    def __init__(self, name, phone, position, department, available="Available"):
        super().__init__(name, phone, position, available)
        self.department = str(department)

    def get_screens(self):
        avail_tag = f"[{self.available[:4]}]"
        s1_l0 = f"{self.name[:10]} {avail_tag:>5}"
        s1_l1 = f"{self.position[:16]:<16}"
        s2_l0 = f"Dept:{self.department[:11]:<11}"
        s2_l1 = f"Ph: {self.phone[:12]:<12}"
        return [(s1_l0, s1_l1), (s2_l0, s2_l1)]


class Administrator(Employee):
    """Administrator with calendar-driven status"""
    def __init__(self, name, phone, position, current_meeting="Meeting", available="Busy"):
        super().__init__(name, phone, position, available)
        self.auto_calendar = True
        self.current_meeting = str(current_meeting)

    def cycleAvailability(self):
        # Auto-calendar controlled; toggles between Busy and Available
        self.available = "Available" if self.available == "Busy" else "Busy"
        return self.available

    def get_screens(self):
        avail_tag = f"[{self.available[:4]}]"
        s1_l0 = f"{self.name[:10]} {avail_tag:>5}"
        s1_l1 = f"{self.position[:16]:<16}"
        s2_l0 = "Cal: Auto Sync"
        s2_l1 = f"{self.current_meeting[:16]:<16}"
        return [(s1_l0, s1_l1), (s2_l0, s2_l1)]


class StudentWorker(Employee):
    """Student worker with supervisor and max hours"""
    def __init__(self, name, phone, position, supervisor, max_hours=20, available="Available"):
        super().__init__(name, phone, position, available)
        self.supervisor = str(supervisor)
        self.max_hours = int(max_hours)

    def get_screens(self):
        avail_tag = f"[{self.available[:4]}]"
        s1_l0 = f"{self.name[:10]} {avail_tag:>5}"
        s1_l1 = f"{self.position[:16]:<16}"
        s2_l0 = f"Sup: {self.supervisor[:11]:<11}"
        s2_l1 = f"Max: {self.max_hours} hrs/wk"
        return [(s1_l0, s1_l1), (s2_l0, s2_l1)]