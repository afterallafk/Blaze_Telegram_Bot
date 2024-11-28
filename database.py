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
    maintainer = input("Enter maintainer name (without @): ").strip()
    sgroup = input("Enter support group (sgroup): ").strip()

    database.append({
        "device": device,
        "codename": codename,
        "maintainer": maintainer,
        "sgroup": sgroup,
    })
    print(f"Device '{device}' with codename '{codename}' added successfully!")

# Edit an existing device's details
def edit_device(database):
    display_devices(database)
    if not database:
        print("No devices available to edit.")
        return
    
    try:
        index = int(input("\nEnter the device number to edit: ").strip()) - 1
        if index < 0 or index >= len(database):
            print("Invalid device number.")
            return

        print("\n--- Edit Device Details ---")
        print(f"Editing device: {database[index]['device']} ({database[index]['codename']})")

        device = input(f"Enter new device name (current: {database[index]['device']}): ").strip() or database[index]['device']
        codename = input(f"Enter new codename (current: {database[index]['codename']}): ").strip() or database[index]['codename']
        maintainer = input(f"Enter new maintainer (current: {database[index]['maintainer']}): ").strip() or database[index]['maintainer']
        sgroup = input(f"Enter new support group (current: {database[index]['sgroup']}): ").strip() or database[index]['sgroup']

        database[index] = {
            "device": device,
            "codename": codename,
            "maintainer": maintainer,
            "sgroup": sgroup
        }
        print(f"Device '{device}' updated successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid device number.")

# Delete an existing device
def delete_device(database):
    display_devices(database)
    if not database:
        print("No devices available to delete.")
        return
    
    try:
        index = int(input("\nEnter the device number to delete: ").strip()) - 1
        if index < 0 or index >= len(database):
            print("Invalid device number.")
            return

        deleted_device = database.pop(index)
        print(f"Device '{deleted_device['device']}' with codename '{deleted_device['codename']}' has been deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid device number.")

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
        print("3. Edit an existing device")
        print("4. Delete an existing device")
        print("5. Save and exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_devices(database)
        elif choice == "2":
            add_device(database)
        elif choice == "3":
            edit_device(database)
        elif choice == "4":
            delete_device(database)
        elif choice == "5":
            save_database(database)
            break
        else:
            print("Invalid choice. Please try again.")

# Allow the script to be manually editable and runnable
if __name__ == "__main__":
    main()
