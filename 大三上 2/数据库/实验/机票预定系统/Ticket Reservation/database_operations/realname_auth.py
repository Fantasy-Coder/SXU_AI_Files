import sqlite3

def create_realname_auth_table(db_path="airline_ticket_system.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS realname_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            idcard TEXT NOT NULL,
            UNIQUE(name, idcard)
        )
    ''')
    conn.commit()
    conn.close()

def insert_realname_auth(name, idcard, db_path="airline_ticket_system.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO realname_auth (name, idcard) VALUES (?, ?)", (name, idcard))
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    create_realname_auth_table()
    # 示例数据
    insert_realname_auth("张三", "110101199001010011")
    insert_realname_auth("李四", "110101199202020022")
    insert_realname_auth("王五", "110101199303030033")