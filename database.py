import sqlite3
def save_message(user_id,role,content):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL)
    ''')
    cursor.execute('''INSERT INTO history(user_id,role,content) VALUES(?, ?, ?)''', (user_id,role,content))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM history WHERE user_id = ?''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role":row[2],"content": row[3]}for row in rows]

def clear_history(user_id):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM history WHERE user_id = ?''', (user_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return "Удалено"
    else:
        return "В истории ничего нет"


def save_note(user_id, text):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS note(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL
    )
    ''')
    cursor.execute('''INSERT INTO note(user_id, text) VALUES(?, ?)''', (user_id,text))
    conn.commit()
    conn.close()

def get_notes(user_id):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM note WHERE user_id = ?''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"text":row[2]} for row in rows]
