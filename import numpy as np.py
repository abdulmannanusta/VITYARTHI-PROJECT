# -- coding: utf-8 --
"""
Campus Event Manager v2.1
Made by Alex (yes I'm sleep deprived)
For the Computer Science club @ uni
Don't judge my code pls it works
"""

import os
import random
import time
from datetime import datetime
import numpy as np
import sympy as sp  # i thought symbolic math would look cool lol

# yeah global variables are bad but whatever this is a small script
events = []
registrations = []  # who signed up where


def cls():
    # lazy way
    os.system('cls' if os.name == 'nt' else 'clear')


def add_new_event():
    cls()
    print("=== ADDING NEW EVENT ===\n")
    title = input("  Event name/title: ").strip()
    if not title:
        print("  bruh you forgot the title")
        time.sleep(1.5)
        return

    while True:
        try:
            date_input = input("  Date (like 2025-12-24): ").strip()
            event_date = datetime.strptime(date_input, "%Y-%m-%d")
            if event_date < datetime.now():
                print("  dude... you can't make an event in the past")
                continue
            break
        except ValueError:
            print("  nah that's not a valid date, try again")

    price = float(input("  Price per ticket (0 if free): "))
    capacity = int(input("  Max people allowed: "))

    event = {
        "id": len(events) + 1,
        "title": title,
        'date': event_date,   # sometimes single sometimes double quotes idk
        "price": price,
        "capacity": capacity,
    }

    events.append(event)
    print(f"\n  Event '{title}' added! ID = {event['id']}")
    time.sleep(1)


def show_all_events():
    cls()
    if not events:
        print("Nothing here yet... go add some events lazy")
        time.sleep(2)
        return

    print("CURRENT EVENTS:\n")
    for ev in events:
        day_name = ev['date'].strftime("%A")
        nice_date = ev['date'].strftime("%B %d, %Y")
        print(f"  {ev['id']}. {ev['title']}")
        print(f"      {nice_date} ({day_name})")
        print(f"      ${ev['price']:.2f} | {ev['capacity']} seats total\n")
    time.sleep(1.5)


def register_someone_register():
    if not events:
        print("\nNo events bro, can't register for nothing\n")
        time.sleep(2)
        return

    show_all_events()
    try:
        chosen = int(input("\nWhich event ID you going to? "))
    except:
        print("\nthat's not even a number my guy")
        time.sleep(1.8)
        return

    the_event = None
    for e in events:
        if e["id"] == chosen:
            the_event = e
            break

    if not the_event:
        print("Event doesn't exist fam")
        time.sleep(1.5)
        return

    name = input("Your name (or nickname): ").strip()
    if not name:
        name = "Mystery Person"

    # check if already registered (case insensitive)
    already = False
    for reg in registrations:
        if reg["student"].lower() == name.lower() and reg["event_id"] == chosen:
            already = True
            break

    if already:
        print(f"\n{name}, you already signed up for this one!")
    else:
        registrations.append({"student": name, "event_id": chosen})
        print(f"\n{name} → registered for \"{the_event['title']}\"! See you there!")

    time.sleep(2)


def list_all_registrations():
    cls()
    if not registrations:
        print("Nobody signed up yet... sadge")
        time.sleep(2)
        return

    print("PEOPLE WHO ARE COMING:\n")
    counter = 1
    for r in registrations:
        # find event name
        event_name = "Deleted Event?"
        for e in events:
            if e["id"] == r["event_id"]:
                event_name = e["title"]
                break
        print(f"  {counter}. {r['student']} → {event_name}")
        counter += 1
    print()
    time.sleep(2)


def generate_fake_attendance():
    if not events:
        return np.array([])

    # make it different every time like real life
    random.seed(int(time.time() * 1000) % 1234567)

    attendance_list = []
    for event in events:
        cap = event["capacity"]
        # 10% chance it's a total flop
        if random.random() < 0.1:
            attendance_list.append(random.randint(2, max(8, cap//5)))
        else:
            # usually pretty full
            min_att = int(cap * 0.65)
            attendance_list.append(random.randint(min_att, cap))

    return np.array(attendance_list)


def show_money_and_stats():
    cls()
    attendance = generate_fake_attendance()

    if len(events) == 0:
        print("No events = no money = sad")
        time.sleep(2)
        return

    print("REVENUE REPORT (fake data but looks legit)\n")
    total_money = 0
    n = sp.Symbol('n')  

    for i, event in enumerate(events):
        people = attendance[i]
        symbolic_rev = event["price"] * n
        real_rev = symbolic_rev.subs(n, people)

        print(f"  {event['title'][:35]:35} | {people:3} × \( {event['price']:6.2f} = \){float(real_rev):8.2f}")
        total_money += float(real_rev)

    print(f"\n  {'TOTAL MONEY MADE':>45} → ${total_money:8.2f}\n")

    
    if len(attendance) > 0:
        winner = np.argmax(attendance)
        print(f"  Most popular → \"{events[winner]['title']}\" with {attendance[winner]} people!\n")

    
    max_cap = max(e["capacity"] for e in events)
    print("  Seat map thingy (■ = taken, ⋅ = empty)\n")
    for i, event in enumerate(events):
        taken = attendance[i]
        print(f"  {event['title'][:25]:25} | {'■'taken}{'⋅'(max_cap-taken)}  ({taken}/{event['capacity']})")
    print()

   
    print("  Days until events:")
    now = datetime.now()
    for e in events:
        if e['date'] >= now:
            days = (e['date'] - now).days
            print(f"    • {e['title'][:30]:30} → {days} days left")
    print()

    input("\nPress Enter to go back...")


def main():
    
    cls()
    print("\n" * 5)
    print("    CAMPUS EVENT MANAGER 3000".center(70))
    print("    loading awesome features...".center(70))
    time.sleep(1.2)
    print("    (actually just clearing screen)".center(70))
    time.sleep(0.8)
    print("    Made with love and redbull".center(70))
    time.sleep(1.5)
    input("\n    Press Enter to begin...".center(70))

    while True:
        cls()
        print("EVENT MANAGER MENU".center(60))
        print("═" * 60)
        print("  1) Add new event")
        print("  2) Show all events")
        print("  3) Register for event")
        print("  4) See who registered")
        print("  5) Revenue & cool stats")
        print("  0) Exit (finally)")
        print("═" * 60)

        choice = input("\n  Pick one → ").strip().lower()

        if choice in ["1", "add"]:
            add_new_event()
        elif choice in ["2", "list", "show"]:
            show_all_events()
            input("\nPress Enter...")
        elif choice in ["3", "reg", "register"]:
            register_someone_register()
        elif choice in ["4", "people", "regs"]:
            list_all_registrations()
            input("\nPress Enter...")
        elif choice in ["5", "stats", "money", "revenue"]:
            show_money_and_stats()
        elif choice in ["0", "exit", "bye", "quit", "q"]:
            cls()
            print("\n\n    Thanks for using my janky system!")
            print("    Don't forget to study for finals")
            print("    (unlike me)\n\n")
            time.sleep(2.5)
            break
        else:
            print("\n  what? try again")
            time.sleep(1.3)



if _name_ == "_main_":
    # easter egg
    if random.random() < 0.05:
        print("Secret message: you're awesome")
        time.sleep(2)
    main()
