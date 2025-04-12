import psycopg2
import csv
from config import load_config



def create_table():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL
        )
        """
    ]
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
            print("Table phonebook created successfully.")



def insert_from_input():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
            conn.commit()
            print("Data inserted.")



def insert_from_csv(filename):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row['name'], row['phone']))
            print("Data inserted from CSV.")



def update_user():
    target_phone = input("Enter phone number to update: ")
    new_name = input("Enter new name (or press Enter to skip): ")
    new_phone = input("Enter new phone (or press Enter to skip): ")

    updates = []
    values = []

    if new_name:
        updates.append("name = %s")
        values.append(new_name)
    if new_phone:
        updates.append("phone = %s")
        values.append(new_phone)

    values.append(target_phone)  

    if not updates:
        print("Nothing to update.")
        return

    sql = f"UPDATE phonebook SET {', '.join(updates)} WHERE phone = %s"

    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            print("User updated.")


def query_users():
    filter_name = input("Enter name to search (or press Enter): ")
    filter_phone = input("Enter phone to search (or press Enter): ")

    query = "SELECT id, name, phone FROM phonebook WHERE TRUE"
    values = []

    if filter_name:
        query += " AND name ILIKE %s"
        values.append(f"%{filter_name}%")
    if filter_phone:
        query += " AND phone LIKE %s"
        values.append(f"%{filter_phone}%")

    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            for row in cur.fetchall():
                print(row)



def delete_user(conn):
    with conn.cursor() as cur:
        phone = input("Enter phone number to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        conn.commit()
        
        if cur.rowcount:
            print("User deleted.")
        else:
            print("No matching user found.")




def main():

    create_table()

    print("\nPhonebook Operations:")
    print("1. Insert data from input")
    print("2. Insert data from CSV")
    print("3. Update user data")
    print("4. Query users")
    print("5. Delete user data")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        insert_from_input()
    elif choice == '2':
        filename = input("Enter CSV filename: ")
        insert_from_csv(filename)
    elif choice == '3':
        update_user()
    elif choice == '4':
        query_users()
    elif choice == '5':
        delete_user()
    elif choice == '6':
        print("Exiting program.")
        return
    else:
        print("Invalid choice.")


    main()


if __name__ == '__main__':
    main()
