import psycopg2
from config import load_config
import csv

def connect():
    """Connects to the PostgreSQL database."""
    config = load_config()
    try:
        return psycopg2.connect(**config)
    except (psycopg2.Error) as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_tables():
    """Creates the contacts and phone_numbers tables if they don't exist."""
    conn = connect()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    contact_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phone_numbers (
                    phone_id SERIAL PRIMARY KEY,
                    contact_id INTEGER NOT NULL REFERENCES contacts(contact_id) ON DELETE CASCADE,
                    phone_number VARCHAR(20) NOT NULL UNIQUE
                )
            """)
            conn.commit()
            print("Tables 'contacts' and 'phone_numbers' created successfully (or already existed).")
        except (psycopg2.Error) as e:
            conn.rollback()
            print(f"Error creating tables: {e}")
        finally:
            if cur:
                cur.close()
            conn.close()

def insert_contact(conn, first_name, last_name=None):
    """Inserts a new contact into the contacts table and returns its ID."""
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (first_name, last_name) VALUES (%s, %s) RETURNING contact_id", (first_name, last_name))
        contact_id = cur.fetchone()[0]
        conn.commit()
        return contact_id
    except (psycopg2.Error) as e:
        conn.rollback()
        print(f"Error inserting contact: {e}")
        return None
    finally:
        if cur:
            cur.close()

def insert_phone_number(conn, contact_id, phone_number):
    """Inserts a phone number for the specified contact_id."""
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO phone_numbers (contact_id, phone_number) VALUES (%s, %s)", (contact_id, phone_number))
        conn.commit()
        return True
    except (psycopg2.Error) as e:
        conn.rollback()
        print(f"Error inserting phone number: {e}")
        return False
    finally:
        if cur:
            cur.close()

def load_from_csv(conn, csv_filepath):
    """Loads data from a CSV file (name, last name, phone)."""
    try:
        with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header if it exists
            for row in reader:
                if len(row) >= 2:
                    first_name = row[0].strip()
                    last_name = row[1].strip() if len(row) > 1 else None
                    phone_number = row[2].strip() if len(row) > 2 else None

                    if first_name:
                        contact_id = insert_contact(conn, first_name, last_name)
                        if contact_id and phone_number:
                            insert_phone_number(conn, contact_id, phone_number)
            conn.commit()
            print(f"Data successfully loaded from '{csv_filepath}'.")
    except FileNotFoundError:
        print(f"Error: File '{csv_filepath}' not found.")
    except (psycopg2.Error) as e:
        conn.rollback()
        print(f"Error loading from CSV: {e}")

def insert_from_console(conn):
    """Inputs name and phone from the console and adds them to the phonebook."""
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name (optional): ").strip() or None
    phone_number = input("Enter phone number: ").strip()

    if first_name and phone_number:
        contact_id = insert_contact(conn, first_name, last_name)
        if contact_id:
            if insert_phone_number(conn, contact_id, phone_number):
                print(f"Contact '{first_name} {last_name if last_name else ''}' with number '{phone_number}' added successfully.")
            else:
                cur = conn.cursor()
                cur.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
                conn.commit()
                print("Error adding phone number, contact deleted.")
                if cur:
                    cur.close()
    else:
        print("First name and phone number are required.")

def update_user(conn):
    """Updates user data (name or phone)."""
    print("\nChoose what you want to update:")
    print("1. Contact name")
    print("2. Phone number")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        contact_id = input("Enter contact ID to update name: ")
        new_first_name = input("Enter new first name: ").strip()
        new_last_name = input("Enter new last name (optional, leave empty to not change): ").strip() or None
        if contact_id.isdigit():
            update_contact(conn, int(contact_id), new_first_name, new_last_name)
        else:
            print("Invalid contact ID.")
    elif choice == '2':
        old_phone = input("Enter old phone number to update: ").strip()
        new_phone = input("Enter new phone number: ").strip()
        update_phone_number(conn, old_phone, new_phone)
    else:
        print("Invalid choice.")

def update_contact(conn, contact_id, new_first_name=None, new_last_name=None):
    """Updates the first name or last name of a contact by their ID."""
    try:
        cur = conn.cursor()
        updates = []
        params = []
        if new_first_name:
            updates.append("first_name = %s")
            params.append(new_first_name)
        if new_last_name is not None:  # Allow updating to NULL
            updates.append("last_name = %s")
            params.append(new_last_name)

        if updates:
            sql = f"UPDATE contacts SET {', '.join(updates)} WHERE contact_id = %s"
            params.append(contact_id)
            cur.execute(sql, params)
            if cur.rowcount > 0:
                conn.commit()
                print(f"Contact with ID {contact_id} updated successfully.")
                return True
            else:
                print(f"Contact with ID {contact_id} not found.")
                return False
        else:
            print("Nothing to update.")
            return False
    except (psycopg2.Error) as e:
        conn.rollback()
        print(f"Error updating contact: {e}")
        return False
    finally:
        if cur:
            cur.close()

def update_phone_number(conn, phone_number, new_phone_number):
    """Updates the phone number by its value."""
    try:
        cur = conn.cursor()
        cur.execute("UPDATE phone_numbers SET phone_number = %s WHERE phone_number = %s", (new_phone_number, phone_number))
        if cur.rowcount > 0:
            conn.commit()
            print(f"Phone number '{phone_number}' updated to '{new_phone_number}' successfully.")
            return True
        else:
            print(f"Phone number '{phone_number}' not found.")
            return False
    except (psycopg2.Error) as e:
        conn.rollback()
        print(f"Error updating phone number: {e}")
        return False
    finally:
        if cur:
            cur.close()

def query_users(conn):
    """Queries contact data with filtering options."""
    print("\nFilter contacts (leave field empty to skip):")
    first_name_filter = input("Filter by first name: ").strip() or None
    last_name_filter = input("Filter by last name: ").strip() or None
    phone_number_filter = input("Filter by phone number: ").strip() or None
    fetch_contacts(conn, first_name_filter, last_name_filter, phone_number_filter)

def fetch_contacts(conn, first_name_filter=None, last_name_filter=None, phone_number_filter=None):
    """Fetches contact data with various filters."""
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.first_name, c.last_name, pn.phone_number
            FROM contacts c
            LEFT JOIN phone_numbers pn ON c.contact_id = pn.contact_id
            WHERE 1=1
        """
        params = []
        if first_name_filter:
            sql += " AND c.first_name ILIKE %s"  # ILIKE for case-insensitive search
            params.append(f"%{first_name_filter}%")
        if last_name_filter:
            sql += " AND c.last_name ILIKE %s"
            params.append(f"%{last_name_filter}%")
        if phone_number_filter:
            sql += " AND pn.phone_number ILIKE %s"
            params.append(f"%{phone_number_filter}%")

        cur.execute(sql, params)
        results = cur.fetchall()
        if results:
            print("\nFound contacts:")
            for row in results:
                print(f"First Name: {row[0]}, Last Name: {row[1] if row[1] else ''}, Phone: {row[2] if row[2] else 'Not specified'}")
        else:
            print("No contacts found matching the criteria.")
    except (psycopg2.Error) as e:
        print(f"Error querying data: {e}")
    finally:
        if cur:
            cur.close()

def delete_user(conn):
    """Deletes user data by name, last name, or phone number."""
    print("\nDelete contact (enter at least one criterion):")
    first_name = input("First name to delete: ").strip() or None
    last_name = input("Last name to delete: ").strip() or None
    phone_number = input("Phone number to delete: ").strip() or None
    delete_contact(conn, first_name, last_name, phone_number)

def delete_contact(conn, first_name=None, last_name=None, phone_number=None):
    """Deletes contact(s) by first name, last name, or phone number."""
    try:
        cur = conn.cursor()
        sql = """
            DELETE FROM contacts
            WHERE contact_id IN (
                SELECT c.contact_id
                FROM contacts c
                LEFT JOIN phone_numbers pn ON c.contact_id = pn.contact_id
                WHERE 1=1
        """
        params = []
        conditions = []
        if first_name:
            conditions.append("c.first_name ILIKE %s")
            params.append(f"%{first_name}%")
        if last_name:
            conditions.append("c.last_name ILIKE %s")
            params.append(f"%{last_name}%")
        if phone_number:
            conditions.append("pn.phone_number = %s")
            params.append(phone_number)

        if conditions:
            sql += " AND " + " AND ".join(conditions) + ")"
            cur.execute(sql, params)
            rows_deleted = cur.rowcount
            conn.commit()
            print(f"Successfully deleted {rows_deleted} contacts.")
        else:
            print("You must specify a first name, last name, or phone number to delete.")
    except (psycopg2.Error) as e:
        conn.rollback()
        print(f"Error deleting contact: {e}")
    finally:
        if cur:
            cur.close()

def search_by_pattern(conn):
    pattern = input("Enter pattern to search (name, surname, or phone part): ").strip()
    if pattern:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
            results = cur.fetchall()
            if results:
                print("\nMatching Contacts:")
                for row in results:
                    print(f"Name: {row[0]}, Last Name: {row[1] or ''}, Phone: {row[2] or 'Not specified'}")
            else:
                print("No matches found.")
        except psycopg2.Error as e:
            print(f"Error during pattern search: {e}")
        finally:
            if cur:
                cur.close()

def paginate_contacts(limit_count, offset_count):
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()

    try:
        # Вызов функции пагинации
        cur.execute("SELECT * FROM get_contacts_paged(%s, %s);", (limit_count, offset_count))
        result = cur.fetchall()
        print("Paginated contacts:", result)

    except Exception as e:
        print("Pagination error:", e)
        conn.rollback()  # Откатить транзакцию в случае ошибки

    finally:
        cur.close()
        conn.close()

def add_or_update_user_proc(conn):
    fname = input("Enter first name: ").strip()
    lname = input("Enter last name (optional): ").strip() or None
    phone = input("Enter phone number: ").strip()
    if fname and phone:
        try:
            cur = conn.cursor()
            cur.execute("CALL add_or_update_user(%s, %s, %s)", (fname, lname, phone))
            conn.commit()
            print("User added or updated successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error: {e}")
        finally:
            if cur:
                cur.close()

def batch_insert_users(conn):
    first_names = []
    last_names = []
    phones = []

    print("Enter multiple contacts (type 'done' as first name to finish):")
    while True:
        first_name = input("  First name: ").strip()
        if first_name.lower() == 'done':
            break
        last_name = input("  Last name (optional): ").strip() or None
        phone = input("  Phone number: ").strip()

        first_names.append(first_name)
        last_names.append(last_name)
        phones.append(phone)

    try:
        cur = conn.cursor()
        cur.execute("CALL batch_insert_users(%s, %s, %s)", (first_names, last_names, phones))
        conn.commit()
        print("Batch insert completed. Check for invalid numbers in NOTICEs.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Batch insert error: {e}")
    finally:
        if cur:
            cur.close()


def delete_by_proc(conn):
    name = input("Enter first name (optional): ").strip() or None
    phone = input("Enter phone number (optional): ").strip() or None
    if name or phone:
        try:
            cur = conn.cursor()
            cur.execute("CALL delete_user_by_criteria(%s, %s)", (name, phone))
            conn.commit()
            print("User(s) deleted by criteria.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error deleting user: {e}")
        finally:
            if cur:
                cur.close()
    else:
        print("You must provide at least one criterion.")


def main():
    """Main function for user interaction."""
    create_tables()
    conn = connect()
    if conn:
        try:
            while True:
                print("\nPhonebook Operations:")
                print("1. Insert data from input")
                print("2. Insert data from CSV")
                print("3. Update user data")
                print("4. Query users")
                print("5. Delete user data")
                print("6. Search by pattern")
                print("7. Paginated query")
                print("8. Add or update user")
                print("9. Batch insert users")
                print("10. Delete by criteria")
                print("11. Exit")


                choice = input("Enter your choice (1-11): ")

                if choice == '1':
                    insert_from_console(conn)
                elif choice == '2':
                    filename = input("Enter CSV filename: ")
                    load_from_csv(conn, filename)
                elif choice == '3':
                    update_user(conn)
                elif choice == '4':
                    query_users(conn)
                elif choice == '5':
                    delete_user(conn)
                elif choice == '6':
                    search_by_pattern(conn)
                elif choice == '7':
                    paginate_contacts(conn)
                elif choice == '8':
                    add_or_update_user_proc(conn)
                elif choice == '9':
                    batch_insert_users(conn)
                elif choice == '10':
                    delete_by_proc(conn)
                elif choice == '11':
                    print("Exiting program.")
                    break
                else:
                    print("Invalid choice.")
        finally:
            conn.close()

if __name__ == '__main__':
    main()