import json
import os

# Define the Blaze version
Blaze_Version = "1.0.0"

# Define the path to the database file
DATABASE_FILE = "devices.json"

# Load the database from file
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: Could not decode JSON. Starting with an empty database.")
    return []

# Save the database to file
def save_database(database):
    with open(DATABASE_FILE, "w") as file:
        json.dump(database, file, indent=4)
        print("Database saved successfully!")

# Add a new device entry interactively
def add_device(database):
    print("\n--- Add New Device ---")
    device = input("Enter device name: ").strip()
    codename = input("Enter device codename: ").strip()
    maintainer = input("Enter maintainer name: ").strip()
    sgroup = input("Enter support group (sgroup): ").strip()

    database.append({
        "device": device,
        "codename": codename,
        "maintainer": maintainer,
        "sgroup": sgroup,
    })
    print(f"Device '{device}' with codename '{codename}' added successfully!")

# Display all devices
def display_devices(database):
    print("\n--- Current Devices ---")
    if not database:
        print("No devices in the database.")
    else:
        for idx, entry in enumerate(database, start=1):
            print(f"{idx}. Device: {entry['device']}, Codename: {entry['codename']}, Maintainer: {entry['maintainer']}, Support Group: {entry['sgroup']}")

# Main menu
def main():
    database = load_database()

    while True:
        print("\n--- Device Database Manager ---")
        print("1. Display all devices")
        print("2. Add a new device")
        print("3. Save and exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_devices(database)
        elif choice == "2":
            add_device(database)
        elif choice == "3":
            save_database(database)
            break
        else:
            print("Invalid choice. Please try again.")

# Allow the script to be manually editable and runnable
if __name__ == "__main__":
    main()
