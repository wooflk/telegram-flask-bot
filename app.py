from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname="login",
        user="postgres",
        password="963600zx",
        host="localhost",
        port="5432"
    )

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_connection()
        cur = conn.cursor()

        if action == 'register':
            try:
                cur.execute("INSERT INTO users (telegram_id, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                message = "ты зареган, купи подпиську"
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                message = "ты уже зареган"
                
        elif action == 'login':
            cur.execute("SELECT * FROM users WHERE telegram_id = %s AND password = %s", (username, password))
            user = cur.fetchone()

            if user:
                cur.execute("SELECT is_buy FROM subscriptions WHERE telegram_id = %s ORDER BY buy_date DESC LIMIT 1", (username,))
                sub = cur.fetchone()
                
                if sub and sub[0]:
                    message = "вход успешен, подписька есть"
                else:
                    message = "купи подписьк "
            else:
                message = "неверный логин или пароль"
        
        cur.close()
        conn.close()

    return render_template("login.html", message=message)

if __name__ == '__main__':
    app.run(debug=True)
