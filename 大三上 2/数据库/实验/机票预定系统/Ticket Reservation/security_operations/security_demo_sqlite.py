"""
实验三：数据库安全与权限（SQLite 版演示，应用层 RBAC）
- 角色：admin / agent / customer
- 权限：按资源-动作校验（flight / orders / customer）
- 操作演示：查询航班、更新票价、删除航班、查询客户、查询订单
运行：python security_operations/security_demo_sqlite.py
前置：确保 airline_ticket_system.db 存在（实验一已生成），若无可在当前目录下创建空库，脚本会自动建表+示例数据。
"""
import os
import sys
import sqlite3
from typing import Dict, Tuple

# 便于复用 db_utils 的存在性检查
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_utils import database_exists  # noqa: E402

DB_NAME = "airline_ticket_system.db"

ROLE_PERMS: Dict[str, set[Tuple[str, str]]] = {
    "admin": {
        ("flight", "select"), ("flight", "insert"), ("flight", "update"), ("flight", "delete"),
        ("orders", "select"), ("orders", "insert"), ("orders", "update"), ("orders", "delete"),
        ("customer", "select"),
    },
    "agent": {
        ("flight", "select"), ("flight", "insert"), ("flight", "update"),
        ("orders", "select"), ("orders", "insert"),
        ("customer", "select"),
        # 不含 delete，演示拒绝
    },
    "customer": {
        ("flight", "select"),
        ("orders", "select"),  # 仅查看自己订单
        # 不授予 customer 表 select
    },
}

USERS = {
    "sysadmin_ticket": "admin",
    "ticket_agent": "agent",
    "ticket_customer": "customer",
}


def check_permission(username: str, resource: str, action: str) -> bool:
    role = USERS.get(username)
    if not role:
        print(f"未知用户: {username}")
        return False
    return (resource, action) in ROLE_PERMS.get(role, set())


def connect_db() -> sqlite3.Connection:
    if not database_exists(DB_NAME):
        # 如果不存在就创建空库
        open(DB_NAME, "a").close()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def migrate_schema(conn: sqlite3.Connection) -> None:
    """增量迁移：为缺失列补齐，避免插入/更新失败。"""
    cur = conn.cursor()
    # Flight 补列
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Flight (
            FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightNo TEXT,
            Airline TEXT,
            Departure TEXT,
            Destination TEXT,
            DepartureTime TEXT,
            ArrivalTime TEXT,
            Price REAL,
            TotalSeats INTEGER DEFAULT 0,
            RemainingSeats INTEGER DEFAULT 0,
            AircraftType TEXT DEFAULT '',
            SeatCount INTEGER DEFAULT 0
        )
        """
    )
    flight_cols = {row[1] for row in cur.execute("PRAGMA table_info(Flight)").fetchall()}
    if "TotalSeats" not in flight_cols:
        cur.execute("ALTER TABLE Flight ADD COLUMN TotalSeats INTEGER DEFAULT 0")
    if "RemainingSeats" not in flight_cols:
        cur.execute("ALTER TABLE Flight ADD COLUMN RemainingSeats INTEGER DEFAULT 0")
    if "AircraftType" not in flight_cols:
        cur.execute("ALTER TABLE Flight ADD COLUMN AircraftType TEXT DEFAULT ''")
    if "SeatCount" not in flight_cols:
        cur.execute("ALTER TABLE Flight ADD COLUMN SeatCount INTEGER DEFAULT 0")

    # Customer 补列
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            IDCard TEXT,
            Phone TEXT,
            Email TEXT,
            Address TEXT
        )
        """
    )

    # Orders 补列
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderNo TEXT,
            CustomerID INTEGER,
            OrderDate TEXT,
            TotalAmount REAL,
            PaymentStatus TEXT,
            OrderStatus TEXT
        )
        """
    )
    orders_cols = {row[1] for row in cur.execute("PRAGMA table_info(Orders)").fetchall()}
    if "CustomerID" not in orders_cols:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Orders_new (
                OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
                OrderNo TEXT,
                CustomerID INTEGER,
                OrderDate TEXT,
                TotalAmount REAL,
                PaymentStatus TEXT,
                OrderStatus TEXT
            )
            """
        )
        common_cols = [c for c in ["OrderID", "OrderNo", "OrderDate", "TotalAmount", "PaymentStatus", "OrderStatus"] if c in orders_cols]
        if common_cols:
            col_list = ",".join(common_cols)
            cur.execute(f"INSERT INTO Orders_new ({col_list}) SELECT {col_list} FROM Orders")
        cur.execute("DROP TABLE Orders")
        cur.execute("ALTER TABLE Orders_new RENAME TO Orders")

    conn.commit()


def ensure_schema_and_seed(conn: sqlite3.Connection) -> None:
    """表为空时填充少量示例数据；不清空已有数据。"""
    cur = conn.cursor()
    if cur.execute("SELECT COUNT(1) FROM Flight").fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO Flight (FlightNo, Airline, Departure, Destination, DepartureTime, ArrivalTime, Price, TotalSeats, RemainingSeats, AircraftType, SeatCount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                ("CA1234", "中国国际航空", "北京", "上海", "2024-12-01 08:00:00", "2024-12-01 10:30:00", 800, 150, 150, "A320", 180),
                ("MU5678", "东方航空", "上海", "广州", "2024-12-01 12:00:00", "2024-12-01 14:30:00", 600, 200, 200, "A321", 200),
                ("CZ3456", "南方航空", "广州", "北京", "2024-12-02 09:00:00", "2024-12-02 11:40:00", 950, 180, 180, "B738", 189),
                ("HU7890", "海南航空", "北京", "深圳", "2024-12-02 15:00:00", "2024-12-02 17:50:00", 850, 160, 160, "A330", 260),
                ("ZH4321", "深圳航空", "深圳", "上海", "2024-12-03 07:00:00", "2024-12-03 09:20:00", 700, 140, 140, "E190", 104),
            ],
        )

    if cur.execute("SELECT COUNT(1) FROM Customer").fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO Customer (Name, IDCard, Phone, Email, Address)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                ("张三", "110101199001011234", "13800138000", "zhangsan@example.com", "北京市海淀区"),
                ("李四", "110101199001011235", "13800138001", "lisi@example.com", "上海市浦东新区"),
            ],
        )

    if cur.execute("SELECT COUNT(1) FROM Orders").fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO Orders (OrderNo, CustomerID, OrderDate, TotalAmount, PaymentStatus, OrderStatus)
            VALUES (?, ?, datetime('now'), ?, '未支付', '待确认')
            """,
            [
                ("ORD0001", 1, 800),
                ("ORD0002", 2, 600),
            ],
        )
    conn.commit()


def demo_select_flights(conn: sqlite3.Connection, user: str) -> None:
    if not check_permission(user, "flight", "select"):
        print("权限不足：不能查询航班")
        return
    cur = conn.execute("SELECT FlightID, FlightNo, Airline, Departure, Destination, Price FROM Flight LIMIT 5")
    rows = cur.fetchall()
    print("航班查询结果:")
    for r in rows:
        print(dict(r))


def demo_update_price(conn: sqlite3.Connection, user: str, flight_id: int, new_price: float) -> None:
    if not check_permission(user, "flight", "update"):
        print("权限不足：不能更新航班价格")
        return
    cur = conn.execute("UPDATE Flight SET Price = ? WHERE FlightID = ?", (new_price, flight_id))
    conn.commit()
    print(f"更新航班 {flight_id} 价格完成，影响行数: {cur.rowcount}")


def demo_delete_flight(conn: sqlite3.Connection, user: str, flight_id: int) -> None:
    if not check_permission(user, "flight", "delete"):
        print("权限不足：不能删除航班")
        return
    cur = conn.execute("DELETE FROM Flight WHERE FlightID = ?", (flight_id,))
    conn.commit()
    print(f"删除航班 {flight_id} 完成，影响行数: {cur.rowcount}")


def demo_select_customer(conn: sqlite3.Connection, user: str, customer_id: int) -> None:
    if not check_permission(user, "customer", "select"):
        print("权限不足：不能查询客户表")
        return
    cur = conn.execute("SELECT CustomerID, Name, Phone FROM Customer WHERE CustomerID = ?", (customer_id,))
    row = cur.fetchone()
    print("客户查询结果:", dict(row) if row else None)


def demo_get_customer_orders(conn: sqlite3.Connection, user: str, customer_id: int) -> None:
    if not check_permission(user, "orders", "select"):
        print("权限不足：不能查询订单")
        return
    cur = conn.execute("SELECT OrderID, OrderNo, CustomerID, TotalAmount, OrderStatus FROM Orders WHERE CustomerID = ?", (customer_id,))
    rows = cur.fetchall()
    print("订单查询结果:")
    for r in rows:
        print(dict(r))


def run_scenario(user: str) -> None:
    print("=" * 60)
    print(f"当前用户: {user} (角色: {USERS.get(user, '未知')})")
    print("=" * 60)
    try:
        conn = connect_db()
        migrate_schema(conn)
        ensure_schema_and_seed(conn)
    except Exception as e:  # noqa: BLE001
        print(f"连接数据库失败: {e}")
        return

    try:
        # 获取可用 ID，保证操作有目标
        flight_id_row = conn.execute("SELECT FlightID FROM Flight ORDER BY FlightID LIMIT 1").fetchone()
        customer_id_row = conn.execute("SELECT CustomerID FROM Customer ORDER BY CustomerID LIMIT 1").fetchone()
        fid = flight_id_row[0] if flight_id_row else None
        cid = customer_id_row[0] if customer_id_row else None

        demo_select_flights(conn, user)
        if fid is not None:
            demo_update_price(conn, user, flight_id=fid, new_price=999.0)
            demo_delete_flight(conn, user, flight_id=fid)
        else:
            print("没有航班数据可更新/删除")

        if cid is not None:
            demo_select_customer(conn, user, customer_id=cid)
            demo_get_customer_orders(conn, user, customer_id=cid)
        else:
            print("没有客户数据可查询/下单")
    finally:
        conn.close()


def main():
    print("实验三（SQLite 版）：安全与权限演示 - 应用层 RBAC")
    print("用户列表：sysadmin_ticket / ticket_agent / ticket_customer")
    user = input("请输入要模拟的用户: ").strip()
    if user not in USERS:
        print("未知用户，请重新运行并输入上述用户之一")
        return
    run_scenario(user)


if __name__ == "__main__":
    main()
