"""
业务服务层：基于既有表结构的机票预订核心操作
- 不修改实体/关系模式，仅通过应用层封装业务逻辑
- 功能：用户/乘客管理、航班搜索、下单购票、支付、退票、改签、订单查询
"""
import base64
import hashlib
import os
import random
import string
import time
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict, Any

from db_utils import DatabaseManager

PAY_UNPAID = "未支付"
PAY_PAID = "已支付"
ORDER_PENDING = "待确认"
ORDER_CONFIRMED = "已确认"
ORDER_CANCELLED = "已取消"
TICKET_VALID = "有效"
TICKET_REFUNDED = "已退票"


def _order_no() -> str:
    return "ORD" + datetime.now().strftime("%Y%m%d%H%M%S") + "".join(random.choices(string.digits, k=3))


def _seat_label(existing: List[str], seat_count: int) -> str:
    used = set(existing)
    for idx in range(1, seat_count + 1):
        candidate = f"E{idx}"
        if candidate not in used:
            return candidate
    raise RuntimeError("无可用座位")


def _seat_index(label: str, seat_count: int, seats_per_row: int = 6) -> int:
    """将座位标签(如1A/12F)转换为索引，校验是否在有效范围。"""
    if not label:
        raise ValueError("座位号为空")
    label = label.strip().upper()
    # 拆分行号与字母
    row_part = ""
    col_part = ""
    for ch in label:
        if ch.isdigit():
            row_part += ch
        else:
            col_part += ch
    if not row_part or not col_part or len(col_part) != 1:
        raise ValueError("座位号格式错误，应为'行号+字母'，如1A")
    row = int(row_part)
    col_idx = ord(col_part) - ord("A")  # A=0, B=1...
    if row <= 0 or col_idx < 0 or col_idx >= seats_per_row:
        raise ValueError("座位号超出可选范围")
    idx = (row - 1) * seats_per_row + (col_idx + 1)
    if idx > seat_count:
        raise ValueError("座位号超过该航班座位数")
    return idx


class TicketingService:
    FAILED_LIMIT = 5
    LOCK_MINUTES = 1

    @staticmethod
    def _hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """PBKDF2 hash with per-user salt."""
        salt_bytes = base64.b64decode(salt) if salt else os.urandom(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 600000)
        return base64.b64encode(salt_bytes).decode(), base64.b64encode(dk).decode()

    def _ensure_security_columns(self) -> None:
        """Add security columns if missing for legacy DBs."""
        cols = self.db.fetch_all("PRAGMA table_info(User)") or []
        names = {c[1] for c in cols}
        if "Salt" not in names:
            self.db.execute("ALTER TABLE User ADD COLUMN Salt TEXT")
        if "FailedAttempts" not in names:
            self.db.execute("ALTER TABLE User ADD COLUMN FailedAttempts INTEGER NOT NULL DEFAULT 0")
        if "LockedUntil" not in names:
            self.db.execute("ALTER TABLE User ADD COLUMN LockedUntil TEXT")

    # ----------- 值机选座相关 -----------
    def list_user_tickets(self, user_id: int) -> list:
        # 查询用户所有未选座的机票（SeatNo为''或NULL或Status=有效，且未选座）
        sql = '''
        SELECT t.TicketID, o.OrderNo, f.FlightNo, f.Departure, f.Destination, f.DepartureTime as Date, p.Name as PassengerName, t.SeatNo
        FROM Ticket t
        JOIN Orders o ON t.OrderID = o.OrderID
        JOIN Flight f ON t.FlightID = f.FlightID
        JOIN Passenger p ON t.PassengerID = p.PassengerID
        WHERE o.ContactID = ? AND t.Status = ?
        '''
        rows = self.db.fetch_all(sql, (user_id, TICKET_VALID)) or []
        # 只返回未选座的票（SeatNo为空或NULL）
        return [
            {
                "TicketID": r[0], "OrderNo": r[1], "FlightNo": r[2], "Departure": r[3], "Destination": r[4], "Date": r[5], "PassengerName": r[6], "SeatNo": r[7]
            }
            for r in rows if not r[7] or r[7] == ''
        ]

    def get_available_seats(self, ticket_id: int) -> list:
        # 根据机票ID查航班，返回未被占用的座位号
        row = self.db.fetch_one("SELECT FlightID FROM Ticket WHERE TicketID=?", (ticket_id,))
        if not row:
            return []
        flight_id = row[0]
        seat_count = self._seat_count(flight_id)
        used = set(self._existing_seats(flight_id))
        # 生成所有座位号（E1, E2...）
        all_seats = [f"E{i}" for i in range(1, seat_count + 1)]
        # 只返回未被占用的座位
        return [s for s in all_seats if s not in used]

    def checkin_seat(self, ticket_id: int, seat_no: str) -> None:
        # 选座，需确保座位未被占用（label格式如1A、2B）
        row = self.db.fetch_one("SELECT FlightID FROM Ticket WHERE TicketID=?", (ticket_id,))
        if not row:
            raise ValueError("机票不存在")
        flight_id = row[0]
        used = set(self._existing_seats(flight_id))
        if seat_no in used:
            raise ValueError("座位已被占用")
        # 更新机票座位号，直接存label
        updated = self.db.execute("UPDATE Ticket SET SeatNo=? WHERE TicketID=?", (seat_no, ticket_id))
        if not updated:
            raise ValueError("选座失败")
    # _existing_seats 也要用label格式
    def _existing_seats(self, flight_id: int) -> List[str]:
        rows = self.db.fetch_all("SELECT SeatNo FROM Ticket WHERE FlightID=?", (flight_id,)) or []
        return [r[0] for r in rows if r[0]]
    def __init__(self, db_path: str = "airline_ticket_system.db"):
        self.db = DatabaseManager(db_path)
        if not self.db.connect():
            raise RuntimeError("数据库连接失败")
        self._ensure_security_columns()
        self._ensure_admin()

    # ------------- 用户与认证 -------------
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one(
            "SELECT UserID, Username, Password, Salt, FailedAttempts, LockedUntil, Name, Phone, Email, RegisterTime FROM User WHERE Username=?",
            (username,),
        )
        if not row:
            return None
        (
            user_id,
            uname,
            stored_pwd,
            stored_salt,
            failed_attempts,
            locked_until,
            name,
            phone,
            email,
            reg_time,
        ) = row

        # 锁定检查：在锁定窗口内直接拒绝登录
        if locked_until:
            lock_dt = None
            try:
                lock_dt = datetime.fromisoformat(locked_until)
            except Exception:
                # 数据异常时，保守起见再锁定一个周期
                lock_dt = datetime.now() + timedelta(minutes=self.LOCK_MINUTES)
            if datetime.now() < lock_dt:
                raise ValueError("账户已锁定，请1分钟后重试")
            # 锁已过期，重置计数
            self.db.execute(
                "UPDATE User SET FailedAttempts=0, LockedUntil=NULL WHERE UserID=?",
                (user_id,),
            )
            failed_attempts = 0

        def verify(pwd: str) -> bool:
            if stored_salt:
                _, calc = self._hash_password(pwd, stored_salt)
                return calc == stored_pwd
            return stored_pwd == pwd

        ok = verify(password)
        if not ok:
            new_failed = (failed_attempts or 0) + 1
            lock_until_val = None
            if new_failed >= self.FAILED_LIMIT:
                lock_until_dt = datetime.now() + timedelta(minutes=self.LOCK_MINUTES)
                lock_until_val = lock_until_dt.isoformat()
                left_msg = "账户已锁定，请1分钟后重试"
            else:
                left = max(0, self.FAILED_LIMIT - new_failed)
                left_msg = f"密码错误，还有{left}次输入机会"
            self.db.execute(
                "UPDATE User SET FailedAttempts=?, LockedUntil=? WHERE UserID=?",
                (new_failed, lock_until_val, user_id),
            )
            raise ValueError(left_msg)

        # 成功：重置计数；若仍为明文则升级为hash
        salt, hashed = (stored_salt, stored_pwd) if stored_salt else self._hash_password(password)
        self.db.execute(
            "UPDATE User SET Salt=?, Password=?, FailedAttempts=0, LockedUntil=NULL WHERE UserID=?",
            (salt, hashed, user_id),
        )

        keys = ["UserID", "Username", "Password", "Salt", "FailedAttempts", "LockedUntil", "Name", "Phone", "Email", "RegisterTime"]
        return dict(zip(keys, (user_id, uname, hashed, salt, 0, None, name, phone, email, reg_time)))

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one(
            "SELECT UserID, Username, Name, Phone, Email, RegisterTime FROM User WHERE UserID=?",
            (user_id,),
        )
        if not row:
            return None
        keys = ["UserID", "Username", "Name", "Phone", "Email", "RegisterTime"]
        return dict(zip(keys, row))

    def update_user_profile(self, user_id: int, name: str, phone: Optional[str], email: Optional[str], idcard: Optional[str] = None) -> None:
        try:
            self.db.conn.execute("BEGIN")
            updated = self.db.execute(
                "UPDATE User SET Name=?, Phone=?, Email=? WHERE UserID=?",
                (name, phone, email, user_id),
            )
            if not updated:
                raise ValueError("用户不存在")
            if idcard:
                # 简单策略：同名只保留当前这一条实名记录
                self.db.execute("DELETE FROM realname_auth WHERE name=?", (name,))
                self.db.execute(
                    "INSERT OR IGNORE INTO realname_auth(name, idcard) VALUES(?,?)",
                    (name, idcard),
                )
            self.db.conn.commit()
        except Exception as exc:  # noqa: BLE001
            self.db.conn.rollback()
            raise exc

    def _ensure_admin(self) -> None:
        if not self.db.fetch_one("SELECT 1 FROM User WHERE Username='admin'"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salt, hashed = self._hash_password("admin123")
            self.db.execute(
                "INSERT INTO User(Username, Password, Salt, FailedAttempts, LockedUntil, Name, Phone, Email, RegisterTime) VALUES(?,?,?,?,?,?,?,?,?)",
                ("admin", hashed, salt, 0, None, "管理员", None, None, now),
            )

    # ------------- 基础信息 -------------
    def register_user(self, username: str, password: str, name: str, phone: str = None, email: str = None) -> int:
        exists = self.db.fetch_one("SELECT UserID FROM User WHERE Username=?", (username,))
        if exists:
            raise ValueError("用户名已存在")
        salt, hashed = self._hash_password(password)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute(
            "INSERT INTO User(Username, Password, Salt, FailedAttempts, LockedUntil, Name, Phone, Email, RegisterTime) VALUES(?,?,?,?,?,?,?,?,?)",
            (username, hashed, salt, 0, None, name, phone, email, now),
        )
        return self.db.get_last_insert_id()

    def change_password(self, user_id: int, current_pwd: str, new_pwd: str) -> None:
        row = self.db.fetch_one("SELECT Password, Salt FROM User WHERE UserID=?", (user_id,))
        if not row:
            raise ValueError("用户不存在")
        stored_pwd, stored_salt = row
        if stored_salt:
            _, calc = self._hash_password(current_pwd, stored_salt)
            if calc != stored_pwd:
                raise ValueError("当前密码不正确")
        else:
            if stored_pwd != current_pwd:
                raise ValueError("当前密码不正确")
        salt, hashed = self._hash_password(new_pwd)
        self.db.execute(
            "UPDATE User SET Password=?, Salt=?, FailedAttempts=0, LockedUntil=NULL WHERE UserID=?",
            (hashed, salt, user_id),
        )

    def add_passenger(self, name: str, id_card: str, phone: str = None, email: str = None) -> int:
        exists = self.db.fetch_one("SELECT PassengerID FROM Passenger WHERE IDCard=?", (id_card,))
        if exists:
            return exists[0]
        self.db.execute(
            "INSERT INTO Passenger(Name, IDCard, Phone, Email) VALUES(?,?,?,?)",
            (name, id_card, phone, email),
        )
        return self.db.get_last_insert_id()

    # ------------- 航班查询 -------------
    def search_flights(
        self,
        departure: Optional[str] = None,
        destination: Optional[str] = None,
        date_prefix: Optional[str] = None,
        airline: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        status: Optional[str] = "正常",
    ) -> List[tuple]:
        sql = "SELECT FlightID, FlightNo, Airline, Departure, Destination, DepartureTime, ArrivalTime, Price, RemainingSeats, Status FROM Flight WHERE 1=1"
        params: List[Any] = []
        if departure:
            sql += " AND Departure=?"
            params.append(departure)
        if destination:
            sql += " AND Destination=?"
            params.append(destination)
        if date_prefix:
            sql += " AND DepartureTime LIKE ?"
            params.append(f"{date_prefix}%")
        if airline:
            sql += " AND Airline LIKE ?"
            params.append(f"%{airline}%")
        if price_min is not None:
            sql += " AND Price>=?"
            params.append(price_min)
        if price_max is not None:
            sql += " AND Price<=?"
            params.append(price_max)
        if status:
            sql += " AND Status=?"
            params.append(status)
        sql += " ORDER BY DepartureTime"
        return self.db.fetch_all(sql, tuple(params)) or []

    # ------------- 购票/订单 -------------
    def _seat_count(self, flight_id: int) -> int:
        row = self.db.fetch_one("SELECT SeatCount FROM Flight WHERE FlightID=?", (flight_id,))
        if not row:
            raise ValueError("航班不存在")
        return int(row[0])

    def _existing_seats(self, flight_id: int) -> List[str]:
        rows = self.db.fetch_all("SELECT SeatNo FROM Ticket WHERE FlightID=?", (flight_id,)) or []
        return [r[0] for r in rows if r[0]]

    def available_seats(self, flight_id: int, seats_per_row: int = 6) -> List[str]:
        """返回按行排序的可用座位标签列表（1A,1B...）。"""
        seat_count = self._seat_count(flight_id)
        used = set(self._existing_seats(flight_id))
        labels: List[str] = []
        for idx in range(1, seat_count + 1):
            row = (idx - 1) // seats_per_row + 1
            col = (idx - 1) % seats_per_row
            label = f"{row}{chr(ord('A') + col)}"
            if label not in used:
                labels.append(label)
        return labels

    def create_order(
        self,
        contact_id: int,
        passengers: List[Dict[str, Any]],
        flight_id: int,
        class_type: str = "经济舱",
        seat_labels: Optional[List[str]] = None,
    ) -> Tuple[int, str]:
        """
        支持一次下单多个乘客，并可提前选座。
        passengers: [{"name","idcard","phone","email"}]
        seat_labels: 与乘客一一对应的座位号列表（可为空，空则待后续值机选座）
        """

        # 校验航班与余座，并获取出发到达时间
        flight = self.db.fetch_one(
            "SELECT Price, RemainingSeats, DepartureTime, ArrivalTime, SeatCount FROM Flight WHERE FlightID=?",
            (flight_id,),
        )
        if not flight:
            raise ValueError("航班不存在")
        price, remaining, departure_time, arrival_time, seat_count = (
            float(flight[0]),
            int(flight[1]),
            flight[2],
            flight[3],
            int(flight[4]),
        )

        seat_labels = seat_labels or []
        if seat_labels and len(seat_labels) != len(passengers):
            raise ValueError("座位数量需与乘客数量一致")

        if len(passengers) > remaining:
            raise ValueError("余座不足")

        # 校验座位合法且未占用
        used = set(self._existing_seats(flight_id))
        normalized_seats: List[Optional[str]] = []
        for seat in seat_labels or [None] * len(passengers):
            if seat is None:
                normalized_seats.append(None)
                continue
            idx = _seat_index(seat, seat_count)
            # 统一存储为原始 label（如1A）
            if seat in used:
                raise ValueError(f"座位已被占用: {seat}")
            normalized_seats.append(seat)
            used.add(seat)

        order_no = _order_no()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_amount = price * len(passengers)

        try:
            self.db.conn.execute("BEGIN")
            self.db.execute(
                "INSERT INTO Orders(OrderNo, ContactID, OrderDate, TotalAmount, PaymentStatus, OrderStatus) VALUES(?,?,?,?,?,?)",
                (order_no, contact_id, now, total_amount, PAY_UNPAID, ORDER_PENDING),
            )
            order_id = self.db.get_last_insert_id()

            for idx, passenger_info in enumerate(passengers):
                pid = self.add_passenger(
                    passenger_info["name"],
                    passenger_info["idcard"],
                    passenger_info.get("phone"),
                    passenger_info.get("email"),
                )
                seat_no = normalized_seats[idx]
                self.db.execute(
                    "INSERT INTO Ticket(FlightID, SeatNo, Price, ClassType, Status, PassengerID, OrderID, DepartureTime, ArrivalTime) VALUES(?,?,?,?,?,?,?,?,?)",
                    (flight_id, seat_no, price, class_type, TICKET_VALID, pid, order_id, departure_time, arrival_time),
                )

            # 购票成功后减少余座
            self.db.execute(
                "UPDATE Flight SET RemainingSeats = RemainingSeats - ? WHERE FlightID = ?",
                (len(passengers), flight_id),
            )
            self.db.conn.commit()
            return order_id, order_no
        except Exception as exc:  # noqa: BLE001
            self.db.conn.rollback()
            raise exc

    def pay_order(self, order_id: int) -> None:
        updated = self.db.execute(
            "UPDATE Orders SET PaymentStatus=?, OrderStatus=? WHERE OrderID=?",
            (PAY_PAID, ORDER_CONFIRMED, order_id),
        )
        if not updated:
            raise ValueError("支付更新失败或订单不存在")

    def cancel_order(self, order_id: int) -> None:
        try:
            self.db.conn.execute("BEGIN")
            # 删除票据以释放座位（触发器会回补余座）
            tickets = self.db.fetch_all("SELECT TicketID FROM Ticket WHERE OrderID=?", (order_id,)) or []
            for tid, in tickets:
                self.db.execute("DELETE FROM Ticket WHERE TicketID=?", (tid,))
            self.db.execute(
                "UPDATE Orders SET OrderStatus=?, PaymentStatus=? WHERE OrderID=?",
                (ORDER_CANCELLED, PAY_UNPAID, order_id),
            )
            self.db.conn.commit()
        except Exception as exc:  # noqa: BLE001
            self.db.conn.rollback()
            raise exc

    def refund_ticket(self, ticket_id: int) -> None:
        try:
            self.db.conn.execute("BEGIN")
            ticket = self.db.fetch_one(
                "SELECT OrderID, Price FROM Ticket WHERE TicketID=?",
                (ticket_id,),
            )
            if not ticket:
                raise ValueError("票据不存在")
            order_id, price = ticket
            # 删除票据释放座位
            self.db.execute("DELETE FROM Ticket WHERE TicketID=?", (ticket_id,))
            # 调整订单金额
            self.db.execute(
                "UPDATE Orders SET TotalAmount = TotalAmount - ? WHERE OrderID=?",
                (price, order_id),
            )
            self.db.conn.commit()
        except Exception as exc:  # noqa: BLE001
            self.db.conn.rollback()
            raise exc

    def reschedule_ticket(self, ticket_id: int, new_flight_id: int, class_type: str = "经济舱") -> None:
        try:
            self.db.conn.execute("BEGIN")
            ticket = self.db.fetch_one(
                "SELECT OrderID, PassengerID, Price FROM Ticket WHERE TicketID=?",
                (ticket_id,),
            )
            if not ticket:
                raise ValueError("票据不存在")
            order_id, passenger_id, old_price = ticket
            # 删除旧票释放座位
            self.db.execute("DELETE FROM Ticket WHERE TicketID=?", (ticket_id,))

            flight = self.db.fetch_one("SELECT Price, RemainingSeats FROM Flight WHERE FlightID=?", (new_flight_id,))
            if not flight:
                raise ValueError("新航班不存在")
            new_price, remaining = float(flight[0]), int(flight[1])
            if remaining <= 0:
                raise ValueError("新航班无座")

            seat = _seat_label(self._existing_seats(new_flight_id), self._seat_count(new_flight_id))
            self.db.execute(
                "INSERT INTO Ticket(FlightID, SeatNo, Price, ClassType, Status, PassengerID, OrderID) VALUES(?,?,?,?,?,?,?)",
                (new_flight_id, seat, new_price, class_type, TICKET_VALID, passenger_id, order_id),
            )
            diff = new_price - old_price
            self.db.execute("UPDATE Orders SET TotalAmount = TotalAmount + ? WHERE OrderID=?", (diff, order_id))
            self.db.conn.commit()
        except Exception as exc:  # noqa: BLE001
            self.db.conn.rollback()
            raise exc

    # ------------- 查询 -------------
    def list_orders(self, contact_id: Optional[int] = None) -> List[tuple]:
        sql = "SELECT OrderID, OrderNo, ContactID, OrderDate, TotalAmount, PaymentStatus, OrderStatus FROM Orders"
        params: List[Any] = []
        if contact_id:
            sql += " WHERE ContactID=?"
            params.append(contact_id)
        sql += " ORDER BY OrderDate DESC"
        return self.db.fetch_all(sql, tuple(params)) or []

    def list_tickets(self, order_id: int) -> List[tuple]:
        return self.db.fetch_all(
            """
            SELECT t.TicketID, f.FlightNo, t.SeatNo, t.Price, t.ClassType, t.Status, p.Name, t.DepartureTime, t.ArrivalTime
            FROM Ticket t
            JOIN Flight f ON t.FlightID = f.FlightID
            JOIN Passenger p ON t.PassengerID = p.PassengerID
            WHERE t.OrderID=?
            """,
            (order_id,),
        )

    def close(self) -> None:
        self.db.close()

    # ------------- 辅助：演示输出 -------------
    def describe_order(self, order_id: int) -> Dict[str, Any]:
        order = self.db.fetch_one(
            "SELECT OrderNo, TotalAmount, PaymentStatus, OrderStatus, OrderDate FROM Orders WHERE OrderID=?",
            (order_id,),
        )
        if not order:
            raise ValueError("订单不存在")
        tickets = self.list_tickets(order_id)
        return {
            "order": order,
            "tickets": tickets,
        }


__all__ = ["TicketingService"]
