import sqlite3


def execute_query(sql_query, data=None, db_path='db.sqlite'):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    if data:
        cur.execute(sql_query, data)
    else:
        cur.execute(sql_query)
    con.commit()
    con.close()

def count_all_symbol(user_id, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT SUM(tokens) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                return data[0]
            else:
                return 0
    except Exception as e:
        print(f"Error: {e}")

def count_all_blocks(user_id, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT SUM(bloсks) FROM messages WHERE (user_id=? AND bloсks<>tokens)''', (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                return data[0]
            else:
                return 0
    except Exception as e:
        print(f"Error: {e}")

