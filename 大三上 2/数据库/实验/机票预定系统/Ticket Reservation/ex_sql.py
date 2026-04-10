import sqlite3

conn = sqlite3.connect("airline_ticket_system.db")
cur = conn.cursor()
cur.execute("DELETE FROM Ticket;")
cur.execute("DELETE FROM Orders;")
cur.execute("DELETE FROM sqlite_sequence WHERE name='Ticket';")
cur.execute("DELETE FROM sqlite_sequence WHERE name='Orders';")
conn.commit()
conn.close()
print("订单和机票数据已清空！")