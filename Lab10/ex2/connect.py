import psycopg2
from config import load_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete_saved_game(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_scores WHERE user_id = %s", (user_id,))
    conn.commit()
    print(f"Сохраненная игра для пользователя с ID {user_id} удалена.")


if __name__ == '__main__':
    config = load_config()
    connect(config)