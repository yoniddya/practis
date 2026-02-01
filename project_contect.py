import csv
import os
from datetime import datetime
from shutil import copy2

CONTACTS_FILE = "contacts.txt.contacts"
BACKUP_DIR = "backups"
EXPORT_FILE = "contacts_export.txt"

FIELDNAMES = ["name", "phone", "email"]


def ensure_files():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def load_contacts():
    contacts = []
    try:
        with open(CONTACTS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # נוודא שדות קיימים
                contacts.append({
                    "name": row.get("name", "").strip(),
                    "phone": row.get("phone", "").strip(),
                    "email": row.get("email", "").strip()
                })
    except FileNotFoundError:
        return []
    return contacts


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for c in contacts:
            writer.writerow(c)


def add_contact(contacts):
    name = input("שם: ").strip()
    if not name:
        print("השם לא יכול להיות ריק.")
        return
    # מניעת כפילויות לפי שם (case-insensitive)
    if any(c["name"].lower() == name.lower() for c in contacts):
        print("כבר קיים איש קשר עם שם זה.")
        return
    phone = input("טלפון: ").strip()
    email = input("אימייל (אופציונלי): ").strip()
    contacts.append({"name": name, "phone": phone, "email": email})
    contacts.sort(key=lambda x: x["name"].lower())
    save_contacts(contacts)
    print("איש קשר נוסף בהצלחה.")


def show_all_contacts(contacts):
    if not contacts:
        print("אין אנשי קשר לשמירה.")
        return
    print("\n=== אנשי קשר ===")
    for i, c in enumerate(sorted(contacts, key=lambda x: x["name"].lower()), start=1):
        print(f"{i}. {c['name']} | טלפון: {c['phone']} | אימייל: {c['email']}")
    print("================\n")


def search_contact(contacts):
    term = input("הכנס שם לחיפוש: ").strip().lower()
    found = [c for c in contacts if term in c["name"].lower()]
    if not found:
        print("לא נמצא איש קשר התואם לחיפוש.")
        return
    print(f"\nנמצאו {len(found)} תוצאות:")
    for c in found:
        print(f"- {c['name']} | טלפון: {c['phone']} | אימייל: {c['email']}")
    print()


def delete_contact(contacts):
    name = input("הכנס שם למחיקה: ").strip()
    matches = [c for c in contacts if c["name"].lower() == name.lower()]
    if not matches:
        print("לא נמצא איש קשר עם שם זה.")
        return
    # אם יש יותר מתוצאה אחת (לא סביר אם מנענו כפילויות), נציג לבחירה
    if len(matches) > 1:
        print("נמצאו מספר אנשי קשר עם שם זה:")
        for idx, c in enumerate(matches, start=1):
            print(f"{idx}. {c['name']} | {c['phone']} | {c['email']}")
        choice = input("בחר מספר למחיקה או לחץ Enter לביטול: ").strip()
        if not choice.isdigit():
            print("בוטל.")
            return
        choice = int(choice) - 1
        to_remove = matches[choice]
    else:
        to_remove = matches[0]

    contacts.remove(to_remove)
    save_contacts(contacts)
    print(f"איש הקשר {to_remove['name']} נמחק בהצלחה.")


def edit_contact(contacts):
    name = input("הכנס שם לעריכה: ").strip()
    matches = [c for c in contacts if c["name"].lower() == name.lower()]
    if not matches:
        print("לא נמצא איש קשר עם שם זה.")
        return
    contact = matches[0]
    print(f"נמצא: {contact['name']} | טלפון: {contact['phone']} | אימייל: {contact['email']}")
    new_phone = input("הכנס טלפון חדש (השאר ריק כדי לא לשנות): ").strip()
    new_email = input("הכנס אימייל חדש (השאר ריק כדי לא לשנות): ").strip()
    if new_phone:
        contact["phone"] = new_phone
    if new_email:
        contact["email"] = new_email
    save_contacts(contacts)
    print("העדכון נשמר.")


def backup_contacts():
    ensure_files()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = os.path.join(BACKUP_DIR, f"contacts_backup_{timestamp}.txt.contacts")
    copy2(CONTACTS_FILE, backup_name)
    print(f"גיבוי נוצר: {backup_name}")


def export_readable(contacts):
    if not contacts:
        print("אין מה לייצא.")
        return
    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        f.write("=== Contact Book Export ===\n\n")
        for i, c in enumerate(sorted(contacts, key=lambda x: x["name"].lower()), start=1):
            f.write(f"{i}. Name: {c['name']}\n")
            f.write(f"   Phone: {c['phone']}\n")
            f.write(f"   Email: {c['email']}\n\n")
    print(f"ייצוא הושלם לקובץ: {EXPORT_FILE}")


def main_menu():
    ensure_files()
    while True:
        contacts = load_contacts()
        print("=== Contact Book ===")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Edit contact")
        print("6. Backup contacts")
        print("7. Export readable")
        print("8. Exit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            show_all_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            edit_contact(contacts)
        elif choice == "6":
            backup_contacts()
        elif choice == "7":
            export_readable(contacts)
        elif choice == "8":
            print("להתראות!")
            break
        else:
            print("בחירה לא תקינה, נסה שוב.")


if __name__ == "__main__":
    main_menu()
