import os

# File to store contact data
db_file = "contacts.txt"

names = [] 
phone_numbers = []

# Load existing contacts from file
if os.path.exists(db_file):
    with open(db_file, "r") as file:
        for line in file:
            name, phone_number = line.strip().split(",")
            names.append(name)
            phone_numbers.append(phone_number)

# Show previously stored records
if names:
    print("\nPrevious Contacts:")
    print("Name\t\t\tPhone Number")
    print("-" * 40)
    for i in range(len(names)):
        print("{:<20}\t{}".format(names[i], phone_numbers[i]))
else:
    print("No previous contacts found.")

# Ask the user how many new contacts to enter
try:
    num = int(input("\nHow many new contacts do you want to add? "))
except ValueError:
    print("Please enter a valid number.")
    exit()

# Input new contacts
with open(db_file, "a") as file:
    for i in range(num):
        print(f"\nContact {i + 1}")
        name = input("Name: ").strip()
        phone_number = input("Phone Number: ").strip()

        names.append(name)
        phone_numbers.append(phone_number)
        file.write(f"{name},{phone_number}\n")

# Display all contacts
print("\nAll Contacts:")
print("Name\t\t\tPhone Number")
print("-" * 40)
for i in range(len(names)):
    print("{:<20}\t{}".format(names[i], phone_numbers[i]))

# Search functionality
while True:
    search_term = input("\nEnter a name to search (or type 'exit' to quit): ").strip()

    if search_term.lower() == 'exit':
        print("Exiting search.")
        break

    print("\nSearch Result:")
    if search_term in names:
        index = names.index(search_term)
        print("Name: {}, Phone Number: {}".format(names[index], phone_numbers[index]))
    else:
        print("404 - User Not Found")
