import sqlite3
import time

# ----------------------------   DATABASE CODES -----------------------------

# Initializing the database and tables
def create_database():
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            vehicle_name TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()

# Function to add a new vehicle entry
def add_vehicle_to_db(vehicle_number, vehicle_type, vehicle_name, owner_name, date, time):
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO vehicles (vehicle_number, vehicle_type, vehicle_name, owner_name, date, time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (vehicle_number, vehicle_type, vehicle_name, owner_name, date, time))

    conn.commit()
    conn.close()

# Function to remove vehicle from the database
def remove_vehicle_from_db(vehicle_number):
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM vehicles WHERE vehicle_number = ?
    ''', (vehicle_number,))

    conn.commit()
    conn.close()

# Function to view all parked vehicles
def view_parked_vehicles():
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vehicles')
    vehicles = cursor.fetchall()

    print("-" * 120)
    print("\t\t\t\tParked Vehicles")
    print("-" * 120)
    print("Vehicle No.\t\tType\t\tName\t\tOwner\t\tDate\t\tTime")
    print("-" * 120)

    for vehicle in vehicles:
        print(f"{vehicle[1]:<18}{vehicle[2]:<20}{vehicle[3]:<15}{vehicle[4]:<15}{vehicle[5]:<15}{vehicle[6]}")
    
    print("-" * 120)
    print(f"Total Records: {len(vehicles)}")
    
    conn.close()

# Function to view available spaces
def view_available_spaces():
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    cursor.execute('SELECT vehicle_type FROM vehicles')
    vehicles = cursor.fetchall()

    spaces = {'Bicycle': 300, 'Bike': 300, 'Car': 300}

    # Count the number of vehicles of each type
    for vehicle in vehicles:
        if vehicle[0] in spaces:
            spaces[vehicle[0]] -= 1

    print("-" * 60)
    print("Spaces Left for Parking")
    print("-" * 60)
    print(f"Bicycles: {spaces['Bicycle']}")
    print(f"Bikes    : {spaces['Bike']}")
    print(f"Cars     : {spaces['Car']}")
    
    conn.close()

# Function to show amount details
def show_amount_details():
    print("-" * 60)
    print("Parking Rates:")
    print("1. Bicycle - ₹ 20/hour")
    print("2. Bike    - ₹ 40/hour")
    print("3. Car     - ₹ 60/hour")

# Function to generate bill
def generate_bill(vehicle_number, hours_parked):
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vehicles WHERE vehicle_number = ?', (vehicle_number,))
    vehicle = cursor.fetchone()

    if vehicle:
        print("\n--- Billing Details ---")
        print("Check-in Time:", vehicle[6])
        print("Check-in Date:", vehicle[5])
        print("Vehicle Type :", vehicle[2])

        if vehicle[2] == 'Bicycle':
            rate = 20
        elif vehicle[2] == 'Bike':
            rate = 40
        else:
            rate = 60

        amount = rate * hours_parked if hours_parked > 0 else rate
        gst = round(0.18 * amount, 2)
        total = amount + gst
        print(f"Base Charge: ₹{amount}")
        print(f"GST (18%)  : ₹{gst}")
        print(f"Total      : ₹{total}")
    else:
        print("### Vehicle not found.")
    
    conn.close()

# Main program
def main():
    create_database()

    try:
        while True:
            print("\n" + "-" * 90)
            print("\t\tParking Management System")
            print("-" * 90)
            print("1. Vehicle Entry")
            print("2. Remove Entry")
            print("3. View Parked Vehicles")
            print("4. View Left Parking Space")
            print("5. Amount Details")
            print("6. Bill")
            print("7. Exit ")
            print("-" * 90)

            ch = input("Select option: ").strip()
            if not ch.isdigit():
                print("### Invalid choice! Please enter a number from 1 to 7.")
                continue
            ch = int(ch)

            # 1. Vehicle Entry
            if ch == 1:
                while True:
                    Vno = input("Enter vehicle number (XXXX-XX-XXXX): ").upper()
                    if Vno == "":
                        print("### Enter Vehicle Number.")
                    elif len(Vno) == 12:
                        break
                    else:
                        print("### Invalid Vehicle Number Format.")

                while True:
                    Vtype = input("Enter vehicle type (Bicycle = A, Bike = B, Car = C): ").lower()
                    if Vtype == "a":
                        vehicle_type = "Bicycle"
                        break
                    elif Vtype == "b":
                        vehicle_type = "Bike"
                        break
                    elif Vtype == "c":
                        vehicle_type = "Car"
                        break
                    else:
                        print("### Invalid Vehicle Type.")

                vname = input("Enter vehicle name: ").strip()
                OName = input("Enter owner name: ").strip()
                date = input("Enter Date (DD-MM-YYYY): ").strip()
                entry_time = input("Enter Time (HH:MM:SS): ").strip()

                add_vehicle_to_db(Vno, vehicle_type, vname, OName, date, entry_time)

                print("\n✅ Vehicle entry recorded successfully!")

            # 2. Remove Entry
            elif ch == 2:
                Vno = input("Enter vehicle number to remove: ").upper()
                remove_vehicle_from_db(Vno)
                print("✅ Vehicle entry removed successfully.")

            # 3. View Parked Vehicles
            elif ch == 3:
                view_parked_vehicles()

            # 4. View Available Space
            elif ch == 4:
                view_available_spaces()

            # 5. Amount Details
            elif ch == 5:
                show_amount_details()

            # 6. Bill
            elif ch == 6:
                Vno = input("Enter vehicle number for billing: ").upper()
                hrs = int(input("Enter number of hours parked: ").strip())
                generate_bill(Vno, hrs)

            # 7. Exit Program
            elif ch == 7:
                print("Thank you for using our Parking Management System. Bye 👋")
                break

            else:
                print("### Invalid option. Please choose between 1 and 7.")

    except Exception as e:
        print("An error occurred:", e)
        main()

main()

# ----------------------------   MAIN CODES -----------------------------

Vehicle_Number = ['XXXX-XX-XXXX']
Vehicle_Type = ['Bike']
vehicle_Name = ['Intruder']
Owner_Name = ['Unknown'] 
Date = ['22-22-3636']
Time = ['22:22:22']

bikes = 300
cars = 300
bicycles = 300

def main():
    global bikes, cars, bicycles
    try:
        while True:
            print("\n" + "-" * 90)
            print("\t\tParking Management System")
            print("-" * 90)
            print("1. Vehicle Entry")
            print("2. Remove Entry")
            print("3. View Parked Vehicles")
            print("4. View Left Parking Space")
            print("5. Amount Details")
            print("6. Bill")
            print("7. Exit ")
            print("-" * 90)

            ch = input("Select option: ").strip()
            if not ch.isdigit():
                print("### Invalid choice! Please enter a number from 1 to 7.")
                continue
            ch = int(ch)

            # 1. Vehicle Entry
            if ch == 1:
                while True:
                    Vno = input("Enter vehicle number (XXXX-XX-XXXX): ").upper()
                    if Vno == "":
                        print("### Enter Vehicle Number.")
                    elif Vno in Vehicle_Number:
                        print("### Vehicle Number Already Exists.")
                    elif len(Vno) == 12:
                        Vehicle_Number.append(Vno)
                        break
                    else:
                        print("### Invalid Vehicle Number Format.")

                while True:
                    Vtype = input("Enter vehicle type (Bicycle = A, Bike = B, Car = C): ").lower()
                    if Vtype == "":
                        print("### Enter Vehicle Type.")
                    elif Vtype == "a":
                        Vehicle_Type.append("Bicycle")
                        bicycles -= 1
                        break
                    elif Vtype == "b":
                        Vehicle_Type.append("Bike")
                        bikes -= 1
                        break
                    elif Vtype == "c":
                        Vehicle_Type.append("Car")
                        cars -= 1
                        break
                    else:
                        print("### Invalid Vehicle Type.")

                while True:
                    vname = input("Enter vehicle name: ").strip()
                    if vname:
                        vehicle_Name.append(vname)
                        break
                    else:
                        print("### Enter Vehicle Name.")

                while True:
                    OName = input("Enter owner name: ").strip()
                    if OName:
                        Owner_Name.append(OName)
                        break
                    else:
                        print("### Enter Owner Name.")

                while True:
                    date = input("Enter Date (DD-MM-YYYY): ").strip()
                    if len(date) == 10:
                        Date.append(date)
                        break
                    else:
                        print("### Invalid Date Format.")

                while True:
                    entry_time = input("Enter Time (HH:MM:SS): ").strip()
                    if len(entry_time) == 8:
                        Time.append(entry_time)
                        break
                    else:
                        print("### Invalid Time Format.")

                print("\n✅ Vehicle entry recorded successfully!")

            # 2. Remove Entry
            elif ch == 2:
                Vno = input("Enter vehicle number to remove: ").upper()
                if len(Vno) == 12 and Vno in Vehicle_Number:
                    i = Vehicle_Number.index(Vno)
                    vtype = Vehicle_Type[i]

                    # Free up space
                    if vtype == "Bicycle": bicycles += 1
                    elif vtype == "Bike": bikes += 1
                    elif vtype == "Car": cars += 1

                    # Remove details
                    Vehicle_Number.pop(i)
                    Vehicle_Type.pop(i)
                    vehicle_Name.pop(i)
                    Owner_Name.pop(i)
                    Date.pop(i)
                    Time.pop(i)
                    print("✅ Vehicle entry removed successfully.")
                else:
                    print("### Vehicle Not Found or Invalid Number.")

            # 3. View Parked Vehicles
            elif ch == 3:
                print("-" * 120)
                print("\t\t\t\tParked Vehicles")
                print("-" * 120)
                print("Vehicle No.\t\tType\t\tName\t\tOwner\t\tDate\t\tTime")
                print("-" * 120)
                for i in range(len(Vehicle_Number)):
                    print(f"{Vehicle_Number[i]:<18}{Vehicle_Type[i]:<20}{vehicle_Name[i]:<15}{Owner_Name[i]:<15}{Date[i]:<15}{Time[i]}")
                print("-" * 120)
                print(f"Total Records: {len(Vehicle_Number)}")

            # 4. View Available Space
            elif ch == 4:
                print("-" * 60)
                print("Spaces Left for Parking")
                print("-" * 60)
                print(f"Bicycles: {bicycles}")
                print(f"Bikes    : {bikes}")
                print(f"Cars     : {cars}")

            # 5. Amount Details
            elif ch == 5:
                print("-" * 60)
                print("Parking Rates:")
                print("1. Bicycle - ₹ 20/hour")
                print("2. Bike    - ₹ 40/hour")
                print("3. Car     - ₹ 60/hour")

            # 6. Bill
            elif ch == 6:
                Vno = input("Enter vehicle number for billing: ").upper()
                if Vno in Vehicle_Number:
                    i = Vehicle_Number.index(Vno)
                    print("\n--- Billing Details ---")
                    print("Check-in Time:", Time[i])
                    print("Check-in Date:", Date[i])
                    print("Vehicle Type :", Vehicle_Type[i])

                    while True:
                        hrs = input("Enter number of hours parked: ").strip()
                        if hrs.isdigit():
                            hrs = int(hrs)
                            if Vehicle_Type[i] == "Bicycle":
                                rate = 20
                            elif Vehicle_Type[i] == "Bike":
                                rate = 40
                            else:
                                rate = 60
                            amount = rate * hrs if hrs > 0 else rate
                            gst = round(0.18 * amount, 2)
                            total = amount + gst
                            print(f"Base Charge: ₹{amount}")
                            print(f"GST (18%)  : ₹{gst}")
                            print(f"Total      : ₹{total}")
                            break
                        else:
                            print("### Please enter valid hours.")
                else:
                    print("### Vehicle not found.")

            # 7. Exit Program
            elif ch == 7:
                print("Thank you for using our Parking Management System. Bye 👋")
                break

            else:
                print("### Invalid option. Please choose between 1 and 7.")

    except Exception as e:
        print("An error occurred:", e)
        main()

main()
# The code is a simple parking management system that allows users to manage vehicle entries, removals, and
# billing. It includes features for viewing parked vehicles and available parking spaces.