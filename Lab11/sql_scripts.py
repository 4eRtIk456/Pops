import psycopg2
from config import load_config

def create_procedures():
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()
        print("Connected to database.")
        
        # Функция поиска по шаблону
        print("Creating: search_by_pattern...")
        try:
            cur.execute("""
                CREATE OR REPLACE FUNCTION search_by_pattern(
                    name_pattern TEXT,
                    surname_pattern TEXT,
                    phone_pattern TEXT
                )
                RETURNS TABLE (
                    first_name TEXT,
                    last_name TEXT,
                    phone_number TEXT
                )
                LANGUAGE SQL
                AS $$
                    SELECT c.first_name, c.last_name, pn.phone_number
                    FROM contacts c
                    LEFT JOIN phone_numbers pn ON c.contact_id = pn.contact_id
                    WHERE (name_pattern IS NULL OR c.first_name ILIKE '%' || name_pattern || '%')
                    AND (surname_pattern IS NULL OR c.last_name ILIKE '%' || surname_pattern || '%')
                    AND (phone_pattern IS NULL OR pn.phone_number ILIKE '%' || phone_pattern || '%');
                $$
            """)
            print("search_by_pattern created.")
        except Exception as e:
            print(f"Error creating search_by_pattern: {e}")
            conn.rollback()

        # Процедура вставки нового пользователя или обновления номера
        print("Creating: insert_or_update_user...")
        try:
            cur.execute("""
                CREATE OR REPLACE PROCEDURE add_or_update_user(
                    fname TEXT,
                    lname TEXT,
                    phone TEXT
                )
                LANGUAGE plpgsql
                AS $$
                DECLARE
                    existing_id INT;
                BEGIN
                    SELECT c.contact_id INTO existing_id
                    FROM contacts c
                    JOIN phone_numbers pn ON c.contact_id = pn.contact_id
                    WHERE c.first_name = fname AND (lname IS NULL OR c.last_name = lname);

                    IF existing_id IS NOT NULL THEN
                        UPDATE phone_numbers SET phone_number = phone WHERE contact_id = existing_id;
                    ELSE
                        INSERT INTO contacts(first_name, last_name)
                        VALUES(fname, lname)
                        RETURNING contact_id INTO existing_id;

                        INSERT INTO phone_numbers(contact_id, phone_number)
                        VALUES(existing_id, phone);
                    END IF;
                END;
                $$
            """)
            print("insert_or_update_user created.")
        except Exception as e:
            print(f"Error creating insert_or_update_user: {e}")
            conn.rollback()

        # Процедура массовой вставки пользователей
        print("Creating: batch_insert_users...")
        try:
            cur.execute(r"""
                CREATE OR REPLACE PROCEDURE batch_insert_users(
                    first_names TEXT[],
                    last_names TEXT[],
                    phones TEXT[]
                )
                LANGUAGE plpgsql
                AS $$
                DECLARE
                    i INT;
                    contact_id INT;
                    bad_phones TEXT[] := ARRAY[]::TEXT[];
                BEGIN
                    IF array_length(first_names, 1) IS NULL THEN
                        RAISE NOTICE 'Empty input arrays.';
                        RETURN;
                    END IF;

                    FOR i IN 1..array_length(first_names, 1) LOOP
                        IF phones[i] IS NULL OR phones[i] !~ '^\+?[0-9\- ]+$' THEN
                            bad_phones := array_append(bad_phones, phones[i]);
                        ELSE
                            SELECT c.contact_id INTO contact_id
                            FROM contacts c
                            JOIN phone_numbers pn ON c.contact_id = pn.contact_id
                            WHERE pn.phone_number = phones[i];

                            IF contact_id IS NULL THEN
                                INSERT INTO contacts(first_name, last_name)
                                VALUES(first_names[i], last_names[i])
                                RETURNING contacts.contact_id INTO contact_id;

                                INSERT INTO phone_numbers(contact_id, phone_number)
                                VALUES(contact_id, phones[i]);
                            END IF;
                        END IF;
                    END LOOP;

                    IF array_length(bad_phones, 1) > 0 THEN
                        RAISE NOTICE 'Invalid phone numbers: %', array_to_string(bad_phones, ', ');
                    END IF;
                END;
                $$;

            """)
            print("batch_insert_users created.")
        except Exception as e:
            print(f"Error creating batch_insert_users: {e}")
            conn.rollback()

        # Функция с пагинацией
        print("Creating: get_contacts_paged...")
        try:
            cur.execute("""
                CREATE OR REPLACE FUNCTION get_contacts_paged(limit_count INT, offset_count INT)
                RETURNS TABLE (
                    first_name TEXT,
                    last_name TEXT,
                    phone_number TEXT
                )
                LANGUAGE SQL
                AS $$
                    SELECT 
                        c.first_name::TEXT,  -- Преобразуем в тип text
                        c.last_name::TEXT,   -- Преобразуем в тип text
                        pn.phone_number::TEXT  -- Преобразуем в тип text
                    FROM contacts c
                    LEFT JOIN phone_numbers pn ON c.contact_id = pn.contact_id
                    ORDER BY c.contact_id
                    LIMIT limit_count OFFSET offset_count;
                $$;

            """)
            print("get_contacts_paged created.")
        except Exception as e:
            print(f"Error creating get_contacts_paged: {e}")
            conn.rollback()

        # Процедура удаления по имени или телефону
        print("Creating: delete_user_by_name_or_phone...")
        try:
            cur.execute("""
                CREATE OR REPLACE PROCEDURE delete_user_by_criteria(
                    fname TEXT,
                    phone TEXT
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    DELETE FROM contacts
                    WHERE contact_id IN (
                        SELECT c.contact_id
                        FROM contacts c
                        LEFT JOIN phone_numbers pn ON c.contact_id = pn.contact_id
                        WHERE (fname IS NOT NULL AND c.first_name ILIKE '%' || fname || '%')
                        OR (phone IS NOT NULL AND pn.phone_number = phone)
                    );
                END;
                $$
            """)
            print("delete_user_by_name_or_phone created.")
        except Exception as e:
            print(f"Error creating delete_user_by_name_or_phone: {e}")
            conn.rollback()

        # Подтверждаем изменения
        conn.commit()
        print("Stored procedures and functions created successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()
        print("Connection closed.")

# Вызов функции
if __name__ == "__main__":
    create_procedures()
