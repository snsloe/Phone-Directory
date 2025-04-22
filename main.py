import json
import re
from datetime import datetime, timedelta

file_phonebook = "phonebook.json"

def creation_file():
    try:
        with open(file_phonebook, "x") as file:
            json.dump([], file)
    except FileExistsError:
        pass

def loading_records():
    try:
        with open(file_phonebook, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def saving_file(phonebook):
    with open(file_phonebook, "w") as file:
        json.dump(phonebook, file, indent=4)

def checking_name(sur_name):
    return re.fullmatch(r"[A-Z][a-zA-Z0-9 ]*", sur_name)

def checking_phone(phone):
    phone = phone.lstrip("+")
    if phone.startswith("7"):
        phone = "8" + phone[1:]
    return re.fullmatch(r"8\d{10}", phone)

def checcking_birthdate(date):
    try:
        parsed_date = datetime.strptime(date, "%d.%m.%Y")
        if parsed_date > datetime.today():
            print("Invalid date: Birth date cannot be in the future.")
            return False
        return True
    except ValueError:
        return False

def format_phone(phone):
    if phone[:2] == "+7":
        return "8" + phone[2:]
    return phone

def finding_record(phonebook, name, surname):
    for record in phonebook:
        if record["name"] == name and record["surname"] == surname:
            return record
    return None

def add_record(phonebook):
    name = input("Enter name: ").capitalize()
    if not checking_name(name):
        print("Invalid name format. Only Latin letters, numbers and spaces, the first letter is uppercase")
        return
    surname = input("Enter surname: ").capitalize()
    if not checking_name(surname):
        print("Invalid surname format. Only Latin letters, numbers and spaces, the first letter is uppercase")
        return
    existing_record = finding_record(phonebook, name, surname)
    if existing_record:
        print("Record with this name and surname already exists.")
        print("1. Update existing record")
        print("2. Change name and surname")
        print("3. Return to menu")
        choice = input("Choose an option: ")
        if choice == "1":
            editing_record(phonebook, name, surname)
        elif choice == "2":
            add_record(phonebook)
        return
    phone = input("Enter phone number (11 digits, starts with 8 or +7): ")
    phone = format_phone(phone)
    if not checking_phone(phone):
        print("Invalid phone number format. 11 digits, starts with 8 or +7")
        return
    birth_date = input("Enter birth date (DD.MM.YYYY) or empty: ")
    if birth_date and not checcking_birthdate(birth_date):
        print("Invalid date format. (DD.MM.YYYY).")
        return
    phonebook.append({
        "name": name,
        "surname": surname,
        "phone": phone,
        "birth_date": birth_date
    })
    print("Record added successfully!")

def show_all(phonebook):
    if not phonebook:
        print("Phonebook is empty.")
        return
    for record in phonebook:
        print(f"Name: {record['name']:<20}| Surname: {record['surname']:<20}| Phone: {format_phone(record['phone']):<15}| Birth Date: {record.get('birth_date', 'N/A')}")

def search_records(phonebook):
    query = input("Enter search query (name, surname, or phone): ").lower()
    results = [record for record in phonebook if query in record["name"].lower() or query in record["surname"].lower() or query in record["phone"]]
    if results:
        for record in results:
            print(f"Name: {record['name']:<15}| Surname: {record['surname']:<15}| Phone: {format_phone(record['phone']):<15}| Birth Date: {record.get('birth_date', 'N/A')}")
    else:
        print("Records not found.")

def deleting_record(phonebook):
    name = input("Enter name to delete: ").capitalize()
    surname = input("Enter surname to delete: ").capitalize()
    record = finding_record(phonebook, name, surname)
    if record:
        phonebook.remove(record)
        print("Record deleted successfully.")
    else:
        print("Record not found.")

def editing_record(phonebook, name=None, surname=None):
    if (not name) or (not surname):
        name = input("Enter name to edit: ").capitalize()
        surname = input("Enter surname to update: ").capitalize()
    record = finding_record(phonebook, name, surname)
    if not record:
        print("Record not found.")
        return
    print("1. Edit name")
    print("2. Edit surname")
    print("3. Edit phone")
    print("4. Edit birth date")
    choice = input("Enter the field to edit: ")
    if choice == "1":
        new_name = input("Enter new name: ").capitalize()
        if not checking_name(new_name):
            print("Invalid name format.")
            return
        record["name"] = new_name
        print("Name edited.")
    elif choice == "2":
        new_surname = input("Enter new surname: ").capitalize()
        if not checking_name(new_surname):
            print("Invalid surname format.")
            return
        record["surname"] = new_surname
        print("Surname edited.")
    elif choice == "3":
        phone = input("Enter new phone number: ")
        phone = format_phone(phone)
        if not checking_phone(phone):
            print("Invalid phone number.")
            return
        record["phone"] = phone
        print("Phone edited.")
    elif choice == "4":
        birth_date = input("Enter new birth date (DD.MM.YYYY): ")
        if not checcking_birthdate(birth_date):
            print("Invalid date format.")
            return
        record["birth_date"] = birth_date
        print("Birth date edited.")
    else:
        print("Invalid choice.")


def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def get_age(phonebook):
    name = input("Enter name: ").capitalize()
    surname = input("Enter surname: ").capitalize()
    record = finding_record(phonebook, name, surname)
    if not record:
        print("Record not found.")
        return
    birth_date = record.get("birth_date")
    if not birth_date:
        print("Birth date not available.")
        return
    age = calculate_age(birth_date)
    print(f"{name} {surname} is {age} years old.")


def get_next_birthday(phonebook):
    today = datetime.today()
    upcoming = None
    for record in phonebook:
        if not record.get("birth_date"):
            continue
        birth_date = datetime.strptime(record["birth_date"], "%d.%m.%Y")
        this_year_birthday = birth_date.replace(year=today.year)
        if this_year_birthday < today:
            this_year_birthday = this_year_birthday.replace(year=today.year + 1)
        if not upcoming or this_year_birthday < upcoming["date"]:
            upcoming = {"record": record, "date": this_year_birthday}
    if upcoming:
        print(
            f"Next birthday: {upcoming['record']['name']} {upcoming['record']['surname']} on {upcoming['date'].strftime('%d.%m.%Y')}")
    else:
        print("No upcoming birthdays found.")


creation_file()
phonebook = loading_records()
while True:
    print("\nPhonebook Menu: \n1. View all records \n2. Search records \n3. Add new record \n4. Delete record \n5. Update record \n6. Get age by name and surname \n7. Get next birthday \n8. Quit")
    choice = input("Enter select option: ")
    if choice == "1":
        show_all(phonebook)
    elif choice == "2":
        search_records(phonebook)
    elif choice == "3":
        add_record(phonebook)
    elif choice == "4":
        deleting_record(phonebook)
    elif choice == "5":
        editing_record(phonebook)
    elif choice == "6":
        get_age(phonebook)
    elif choice == "7":
        get_next_birthday(phonebook)
    elif choice == "8":
        saving_file(phonebook)
        print("Work is completed.")
        break
    else:
        print("Invalid choice. Try again.")

