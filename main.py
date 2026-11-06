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


waiting_requests = []
request_counter = 0

while True:
    print()
    print("1. Add a ride request")
    print("2. View waiting students and all cabs")
    print("3. Quit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        name = ask_name()
        destination = ask_choice("Destination (Delhi/Jaipur): ", DESTINATIONS)
        time_slot = ask_choice("Time slot (Morning/Afternoon/Evening/Night): ", TIME_SLOTS)
        year = ask_year()

        request_counter = request_counter + 1
        new_request = RideRequest(name, destination, time_slot, year, request_counter)
        waiting_requests.append(new_request)

        print("Added", name, "to the waiting list for", destination + ",", time_slot)

    elif choice == "2":
        if len(waiting_requests) == 0:
            print("No requests yet")
        else:
            print("Waiting Requests:")
            for request in waiting_requests:
                print("-", request.name, "|", request.destination + ", " + request.time_slot, "| Year", request.year)

    elif choice == "3":
        print("Bye!")
        break

    else:
        print("Please enter 1, 2 or 3")