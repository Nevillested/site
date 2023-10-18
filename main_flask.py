from flask import Flask, render_template, jsonify
import psycopg2
import time
import cfg

app = Flask(__name__)


# Конфигурация PostgreSQL
db_config = cfg.db_config

def get_messages_from_database():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
    SELECT case when b.username is null then 'аноним' else b.username end || ' ' ||
           case
             when a.message_type = 'text'
               then ' написал сообщение: "' || a.msg_txt_data || '"'
             when a.message_type = 'button'
               then 'ковыряется в меню с ' || case when a.button_id like '1%'
                                                then 'Шинобу'
                                                   when a.button_id like '2%'
                                                then 'музыкой'
                                                   when a.button_id like '3%'
                                                then 'подписками'
                                                   when a.button_id like '4%'
                                                then 'напоминалками'
                                                   when a.button_id like '5%'
                                                then 'шифрованием / дешифрованием'
                                                   when a.button_id like '6%'
                                                then 'изчением японского'
                                                   when a.button_id like '7%'
                                                then 'донатом'
                                                   when a.button_id like '8%'
                                                then 'перевод войса в текст и наоборот'
                                                   when a.button_id like '9%'
                                                then 'полезностями'
                                              end
             when a.message_type = 'voice'
               then 'прислал войс'
             when a.message_type = 'audio'
               then 'прислал аудио'
             when a.message_type = 'video'
               then 'прислал видео'
             when a.message_type = 'photo'
               then 'прислал пикчу'
             when a.message_type = 'sticker'
               then 'прислал стикос'
             when a.message_type = 'video_note'
               then 'прислал видеокруг'
             when a.message_type = 'location'
               then 'прислал локацию'
             when a.message_type = 'contact'
               then 'прислал контакт'
             when a.message_type = 'pinned_message'
               then 'запинил сообщение'
           end
           FROM arabot.income_data as a
           JOIN arabot.users as b
            on a.chat_id = b.chat_id
           ORDER BY a.id DESC
           LIMIT 5
    """)
    messages = [row[0] for row in cur.fetchall()]
    conn.close()
    return messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_messages')
def get_messages():
    messages = get_messages_from_database()
    return jsonify(messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)