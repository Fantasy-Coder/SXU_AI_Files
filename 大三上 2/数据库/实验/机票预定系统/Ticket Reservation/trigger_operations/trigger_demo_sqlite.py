"""
实验四：触发器演示（SQLite 版，机票预订系统）
- 不修改既有实体/关系模式；仅新增审计表并创建触发器。
- 触发器基于现有表字段：User / Passenger / Flight / Orders / Ticket。
- 作用：
  1) BEFORE INSERT ON Ticket：检查航班余座，余座<=0 则拒绝。
  2) AFTER INSERT ON Ticket：减少对应航班剩余座位。
  3) AFTER DELETE ON Ticket：恢复对应航班剩余座位。
  4) BEFORE UPDATE OF Price ON Flight：记录价格变更历史（PriceHistory）。
  5) AFTER UPDATE OF PaymentStatus ON Orders：记录支付状态变更（OrderAudit）。

运行：
  python trigger_operations/trigger_demo_sqlite.py

验证：
  - 插入/删除 Ticket 观察 Flight.RemainingSeats 变化。
  - 更新 Flight.Price 观察 PriceHistory 记录。
  - 更新 Orders.PaymentStatus 观察 OrderAudit 记录。
"""
import os
import sys
import sqlite3
from typing import Dict, Set

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_utils import database_exists  # noqa: E402

DB_NAME = "airline_ticket_system.db"

REQUIRED_SCHEMAS: Dict[str, Set[str]] = {
    "User": {"UserID", "Username", "Password", "Name", "Phone", "Email", "RegisterTime"},
    "Passenger": {"PassengerID", "Name", "IDCard", "Phone", "Email"},
    "Flight": {
        "FlightID",
        "FlightNo",
        "Airline",
        "Departure",
        "Destination",
        "DepartureTime",
        "ArrivalTime",
        "AircraftType",
        "SeatCount",
        "RemainingSeats",
        "Price",
        "Status",
    },
    "Orders": {
        "OrderID",
        "OrderNo",
        "ContactID",
        "OrderDate",
        "TotalAmount",
        "PaymentStatus",
        "OrderStatus",
    },
    "Ticket": {
        "TicketID",
        "FlightID",
        "SeatNo",
        "Price",
        "ClassType",
        "Status",
        "PassengerID",
        "OrderID",
    },
}


def connect_db() -> sqlite3.Connection:
    if not database_exists(DB_NAME):
        raise SystemExit("数据库不存在，请先运行 database_operations/create_database.py 与 table_operations/create_tables.py")
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def validate_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    for table, required_cols in REQUIRED_SCHEMAS.items():
        cur.execute("PRAGMA table_info(%s)" % table)
        cols = {r[1] for r in cur.fetchall()}
        missing = required_cols - cols
        if missing:
            raise SystemExit(f"表 {table} 缺少字段: {missing}，请检查是否已按 create_tables.py 创建")


def create_aux_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS PriceHistory (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightID INTEGER NOT NULL,
            OldPrice REAL NOT NULL,
            NewPrice REAL NOT NULL,
            ChangedAt TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS OrderAudit (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Event TEXT NOT NULL,
            OrderID INTEGER NOT NULL,
            OldStatus TEXT,
            NewStatus TEXT,
            OccurredAt TEXT NOT NULL
        )
        """
    )
    conn.commit()


def create_triggers(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    # 1) 购票前检查余座
    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_ticket_check_seat
        BEFORE INSERT ON Ticket
        BEGIN
            SELECT CASE
                WHEN (SELECT RemainingSeats FROM Flight WHERE FlightID = NEW.FlightID) <= 0
                THEN RAISE(ABORT, 'No seats available for this flight')
            END;
        END;
        """
    )
    # 2) 购票后减少余座
    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_ticket_after_insert
        AFTER INSERT ON Ticket
        BEGIN
            UPDATE Flight SET RemainingSeats = RemainingSeats - 1 WHERE FlightID = NEW.FlightID;
        END;
        """
    )
    # 3) 退票/取消后恢复余座
    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_ticket_after_delete
        AFTER DELETE ON Ticket
        BEGIN
            UPDATE Flight SET RemainingSeats = RemainingSeats + 1 WHERE FlightID = OLD.FlightID;
            -- 联动订单金额与状态，标记退款中，并将订单金额扣减对应票价；若所有票都被删除则标记订单已取消
            UPDATE Orders
              SET TotalAmount = CASE WHEN TotalAmount - OLD.Price < 0 THEN 0 ELSE TotalAmount - OLD.Price END,
                  PaymentStatus = CASE WHEN PaymentStatus = '已支付' THEN '退款中' ELSE PaymentStatus END,
                  OrderStatus = CASE WHEN (SELECT COUNT(1) FROM Ticket WHERE OrderID = OLD.OrderID) = 0 THEN '已取消' ELSE OrderStatus END
              WHERE OrderID = OLD.OrderID;
        END;
        """
    )
    # 4) 票价更新审计
    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_flight_price_history
        BEFORE UPDATE OF Price ON Flight
        BEGIN
            INSERT INTO PriceHistory(FlightID, OldPrice, NewPrice, ChangedAt)
            VALUES (old.FlightID, old.Price, new.Price, datetime('now'));
        END;
        """
    )
    # 5) 支付状态审计
    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_orders_payment_audit
        AFTER UPDATE OF PaymentStatus ON Orders
        BEGIN
            INSERT INTO OrderAudit(Event, OrderID, OldStatus, NewStatus, OccurredAt)
            VALUES ('PAYMENT_STATUS_CHANGE', old.OrderID, old.PaymentStatus, new.PaymentStatus, datetime('now'));
        END;
        """
    )
    conn.commit()


def main():
    print("实验四：SQLite 触发器配置开始……")
    conn = connect_db()
    try:
        validate_schema(conn)
        create_aux_tables(conn)
        create_triggers(conn)
        print("触发器配置完成。建议：插入/删除 Ticket，更新 Flight.Price、更新 Orders.PaymentStatus 进行验证。")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
