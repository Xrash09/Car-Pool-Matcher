import json
import heapq
from models import Cab, RideRequest

DESTINATIONS = ["Delhi", "Jaipur"]
TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]


def ask_choice(question, options):
    while True:
        answer = input(question).strip().capitalize()
        if answer in options:
            return answer
        print("Sorry, please choose one of:", ", ".join(options))


def ask_year():
    while True:
        text = input("Year (1-5): ").strip()
        try:
            year = int(text)
        except ValueError:
            print("Please enter a number, like 2.")
            continue
        if year >= 1 and year <= 5:
            return year
        print("Year must be between 1 and 5.")


def ask_name():
    while True:
        name = input("Name: ").strip()
        if name != "":
            return name
        print("Name can't be empty.")

def load_cabs(filename):
    try:
        with open(filename) as f:
            cab_list = json.load(f)       
    except FileNotFoundError:
        print("Could not find", filename, "- starting with no cabs.")
        return []
    except json.JSONDecodeError:
        print(filename, "is not valid JSON - starting with no cabs.")
        return []

    cabs = []
    try:
        for cab_data in cab_list:
            new_cab = Cab(
                cab_data["driver_name"],
                cab_data["number_of_seats"],
                cab_data["destination"],
                cab_data["time_slot"],
            )
            cabs.append(new_cab)
    except KeyError as missing:
        print("A cab in", filename, "is missing the field", missing, "- starting with no cabs.")
        return []
    return cabs


def dispatch_cab(cabs, waiting):
    destination = ask_choice("Destination (Delhi/Jaipur): ", DESTINATIONS)
    time_slot = ask_choice("Time slot (Morning/Afternoon/Evening/Night): ", TIME_SLOTS)
    trip = (destination, time_slot)

    if trip not in waiting or len(waiting[trip]) == 0:
        print("Nobody is waiting for", destination + ",", time_slot)
        return

    chosen_cab = None
    for cab in cabs:

        if not cab.has_left and cab.destination == destination and cab.time_slot == time_slot:
            chosen_cab = cab
            break

    if chosen_cab is None:
        print("No open cab for", destination + ",", time_slot, "- students keep waiting.")
        return

    free_seats = chosen_cab.number_of_seats - len(chosen_cab.students)
    while free_seats > 0 and len(waiting[trip]) > 0:
        entry = heapq.heappop(waiting[trip])
        chosen_cab.students.append(entry[2])
        free_seats = free_seats - 1

    chosen_cab.has_left = True
    print(chosen_cab.driver_name + "'s cab has left for", destination + ",", time_slot, "with:")
    for student in chosen_cab.students:
        print("-", student.name, "(Year", str(student.year) + ")")

def find_matches(cabs, waiting):
    copies = {}
    anything_shown = False

    for cab in cabs:
        if cab.has_left:
            continue                          

        trip = (cab.destination, cab.time_slot)
        if trip not in copies:
            if trip in waiting:
                copies[trip] = list(waiting[trip])   
            else:
                copies[trip] = []

        free_seats = cab.number_of_seats - len(cab.students)
        would_get_in = []
        while free_seats > 0 and len(copies[trip]) > 0:
            entry = heapq.heappop(copies[trip])            
            would_get_in.append(entry[2])
            free_seats = free_seats - 1

        anything_shown = True
        print(cab.driver_name, "|", cab.destination + ", " + cab.time_slot, "would take:")
        if len(would_get_in) == 0:
            print("  (nobody waiting)")
        for student in would_get_in:
            print("  -", student.name, "(Year", str(student.year) + ")")

    if not anything_shown:
        print("No open cabs")

waiting = {}
cabs = load_cabs("cabs.json")
request_counter = 0

while True:
    print()
    print("1. Add a ride request")
    print("2. View waiting students and all cabs")
    print("3. Find matches")
    print("4. Dispatch a cab")
    print("5. Quit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        name = ask_name()
        destination = ask_choice("Destination (Delhi/Jaipur): ", DESTINATIONS)
        time_slot = ask_choice("Time slot (Morning/Afternoon/Evening/Night): ", TIME_SLOTS)
        year = ask_year()

        request_counter = request_counter + 1
        new_request = RideRequest(name, destination, time_slot, year, request_counter)

        trip = (destination, time_slot)
        if trip not in waiting:
            waiting[trip] = []       
        entry = (5 - year, request_counter, new_request)
        heapq.heappush(waiting[trip], entry)

        print("Added", name, "to the waiting list for", destination + ",", time_slot)

    elif choice == "2":
        
        anyone_waiting = False
        print("Waiting Requests:")
        for trip in waiting:
            for entry in sorted(waiting[trip]):
                request = entry[2]          
                print("-", request.name, "|", request.destination + ", " + request.time_slot, "| Year", request.year)
                anyone_waiting = True
        if not anyone_waiting:
            print("No requests yet")

        print()
        if len(cabs) == 0:
            print("No cabs loaded")
        else:
            print("Cabs:")
            for cab in cabs:
                seats_taken = len(cab.students)
                if cab.has_left:
                    status = "Left"
                else:
                    status = "Open"
                print("-", cab.driver_name, "|", cab.destination + ", " + cab.time_slot, "|", str(seats_taken) + "/" + str(cab.number_of_seats), "|", status)  
    
    elif choice == "3":
        find_matches(cabs, waiting)

    elif choice == "4":
        dispatch_cab(cabs, waiting)

    elif choice == "5":
        print("Bye!")
        break

    else:
        print("Please enter a number 1-5")