import telebot
import psycopg2
from datetime import datetime

TOKEN = 'ughhhhhhhhhhhhhhhhh'
bot = telebot.TeleBot(TOKEN)

def get_connection():
    return psycopg2.connect(
        dbname="login",
        user="postgres",
        password="963600zx",
        host="localhost",
        port="5432"
    )

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = str(message.from_user.id)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO subscriptions (telegram_id, buy_date, is_buy)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING
    ''', (user_id, now, True))

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(msg.chat.id, "подписка успешно куплена!")

bot.polling()
