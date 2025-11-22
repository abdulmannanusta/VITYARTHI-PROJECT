import numpy as np
import sympy as sp
from datetime import datetime
import os

events = []
registrations = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_event():
    title = input("Event title: ")
    date = input("Event date (YYYY-MM-DD): ")
    price = float(input("Price: "))
    capacity = int(input("Capacity: "))
    event = {
        "id": len(events) + 1,
        "title": title,
        "date": datetime.strptime(date, "%Y-%m-%d"),
        "price": price,
        "capacity": capacity
    }
    events.append(event)
    print("Event added!\n")

def list_events():
    print("\nEvents:")
    for e in events:
        print(f"{e['id']}: {e['title']} on {e['date'].strftime('%Y-%m-%d')} | Price: {e['price']} | Capacity: {e['capacity']}")

def register_event():
    student = input("Your name: ")
    event_id = int(input("Event ID: "))
    registration = {
        "student": student,
        "event_id": event_id
    }
    registrations.append(registration)
    print("Registered!\n")

def list_registrations():
    print("\nRegistrations:")
    for r in registrations:
        print(r)

def get_attendance_array():
    # Demo attendance per event: each event gets a random number up to capacity
    if not events:
        return np.array([])
    np.random.seed(1)
    attends = np.random.randint(1, [e["capacity"] + 1 for e in events])
    return attends

def revenue_stats():
    attendance = get_attendance_array()
    total = 0
    print("\nRevenue:")
    for idx, event in enumerate(events):
        n = sp.Symbol('n')
        formula = event['price'] * n
        rev = formula.subs(n, attendance[idx]) if attendance.size > idx else 0
        print(f"Revenue for {event['title']}: {rev}")
        total += rev
    print(f"Total revenue from all events: {total}")

def show_stats():
    attendance = get_attendance_array()
    if attendance.size == 0:
        print("No events available for stats.")
        return
    print(f"Event with max attendance: {events[int(np.argmax(attendance))]['title']}")
    print(f"Average attendance per event: {np.mean(attendance):.2f}")
    seat_matrix = np.zeros((len(events), max(e["capacity"] for e in events)))
    for i, attended in enumerate(attendance):
        seat_matrix[i, :attended] = 1
    print("\nSeat allocation matrix (1=filled, 0=empty):")
    print(seat_matrix)
    now = datetime.now()
    print(f"\nToday's date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    for event in events:
        days_left = (event["date"] - now).days
        print(f"Days left until {event['title']}: {days_left} days")

def menu():
    while True:
        clear_screen()
        print("== Campus Event Manager ==")
        print("1. Add event")
        print("2. List events")
        print("3. Register for event")
        print("4. List registrations")
        print("5. Analytics & Revenue")
        print("0. Exit")
        choice = input("\nEnter choice: ")

        if choice == "1":
            add_event()
            input("Press ENTER to continue...")
        elif choice == "2":
            list_events()
            input("Press ENTER to continue...")
        elif choice == "3":
            list_events()
            register_event()
            input("Press ENTER to continue...")
        elif choice == "4":
            list_registrations()
            input("Press ENTER to continue...")
        elif choice == "5":
            revenue_stats()
            show_stats()
            input("Press ENTER to continue...")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press ENTER to continue...")

if __name__ == "__main__":
    menu()

