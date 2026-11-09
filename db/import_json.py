import sqlite3
import json
import os

DB_PATH = "db/debt_tracker.sqlite"

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    with open("sql/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def import_data():
    conn = sqlite3.connect(DB_PATH)
    
    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    conn.executemany("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", 
                     [(u['id'], u['name'], u['email']) for u in users])
                     
    with open("data/debtors.json", "r", encoding="utf-8") as f:
        debtors = json.load(f)
    conn.executemany("INSERT INTO debtors (id, name, phone) VALUES (?, ?, ?)", 
                     [(d['id'], d['name'], d['phone']) for d in debtors])
                     
    with open("data/debts.json", "r", encoding="utf-8") as f:
        debts = json.load(f)
    conn.executemany("INSERT INTO debts (id, user_id, debtor_id, amount, issue_date, is_paid) VALUES (?, ?, ?, ?, ?, ?)", 
                     [(d['id'], d['user_id'], d['debtor_id'], d['amount'], d['issue_date'], int(d['is_paid'])) for d in debts])
    
    conn.commit()
    conn.close()
    print("База данных создана и данные импортированы.")

if __name__ == "__main__":
    create_db()
    import_data()