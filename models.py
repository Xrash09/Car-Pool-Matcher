class RideRequest:
    def __init__(self, name, destination, time_slot, year, submit_time):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submit_time = submit_time

class Cab:
    def __init__(self, driver_name, number_of_seats, destination, time_slot):
        self.driver_name = driver_name
        self.number_of_seats = number_of_seats
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.students = []