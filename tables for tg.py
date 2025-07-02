import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="login",
        user="postgres",
        password="963600zx",
        host="localhost",
        port="5432"
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            password TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT REFERENCES users(telegram_id),
            buy_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_buy BOOLEAN DEFAULT FALSE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("таблицы успешно созданы")

if __name__ == "__main__":
    create_tables()
