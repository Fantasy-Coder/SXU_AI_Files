"""
实验二：游标功能实现
功能：演示SQLite游标操作，包括声明、打开、读取、更新、事务处理、关闭等操作。
"""
import os
import sys
from typing import Any

# 将项目根目录加入路径，便于导入 db_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists  # noqa: E402


def _print_cursor_meta(cursor: Any) -> None:
    """打印游标元信息，避免未实现属性导致异常。"""
    closed_attr = getattr(cursor, "closed", None)
    if closed_attr is None:
        print("游标是否关闭: (sqlite3 未提供 closed 属性，手动关闭见下)")
    else:
        print(f"游标是否关闭: {closed_attr}")

    rowcount_attr = getattr(cursor, "rowcount", None)
    if rowcount_attr is None:
        print("上次操作影响的行数: (未提供 rowcount 属性)")
    else:
        print(f"上次操作影响的行数: {rowcount_attr}")

    if getattr(cursor, "description", None):
        print(f"当前查询结果列数: {len(cursor.description)}")
        print("查询结果列名:")
        for desc in cursor.description:
            print(f"  - {desc[0]}")
    else:
        print("当前查询结果列数: 0")


def cursor_basic_operations():
    """基本游标操作演示"""
    print("\n=== 基本游标操作演示 ===")

    if not database_exists():
        print("错误: 数据库不存在！请先创建数据库和表结构")
        return

    db = DatabaseManager()
    if not db.connect():
        return

    cursor = None
    try:
        # 获取游标对象
        cursor = db.conn.cursor()
        print("成功获取游标对象")

        # 演示1：使用游标查询航班数据（向前滚动）
        print("\n【演示1：向前滚动查询航班数据】")
        cursor.execute(
            "SELECT FlightID, FlightNo, Airline, Departure, Destination "
            "FROM Flight ORDER BY DepartureTime"
        )

        print("获取单条记录（fetchone）:")
        first_row = cursor.fetchone()
        if first_row:
            print(f"第一条记录: {first_row}")
        else:
            print("没有记录可读取")

        print("\n获取多条记录（fetchmany(2)）:")
        next_rows = cursor.fetchmany(2)
        if next_rows:
            for i, row in enumerate(next_rows, 1):
                print(f"第{i+1}条记录: {row}")
        else:
            print("没有更多记录")

        print("\n获取剩余所有记录（fetchall）:")
        remaining_rows = cursor.fetchall()
        if remaining_rows:
            for i, row in enumerate(remaining_rows, len(next_rows) + 1):
                print(f"第{i+1}条记录: {row}")
        else:
            print("没有剩余记录")

        # 演示2：使用游标修改数据
        print("\n【演示2：使用游标修改数据】")
        flight_id = input("请输入要更新的航班ID: ")
        new_price_input = input("请输入新的票价: ")
        try:
            new_price = float(new_price_input)
        except ValueError:
            print("票价输入无效，操作已取消")
            return

        cursor.execute(
            """
            UPDATE Flight 
            SET Price = ? 
            WHERE FlightID = ?
            """,
            (new_price, flight_id),
        )
        db.conn.commit()
        print(f"已使用游标更新航班ID为{flight_id}的票价")

        # 验证更新结果
        cursor.execute("SELECT FlightNo, Price FROM Flight WHERE FlightID = ?", (flight_id,))
        result = cursor.fetchone()
        if result:
            print(f"更新后的值: 航班号={result[0]}, 新票价={result[1]}")
        else:
            print("未找到对应航班，无法验证更新结果")

        # 演示3：使用游标进行事务处理
        print("\n【演示3：游标事务处理】")
        try:
            db.conn.execute("BEGIN TRANSACTION")

            # 减少航班剩余座位
            cursor.execute(
                """
                UPDATE Flight 
                SET RemainingSeats = RemainingSeats - 1 
                WHERE FlightID = ?
                """,
                (flight_id,),
            )

            # 创建新订单
            new_order_no = f"ORD{os.urandom(4).hex().upper()}"
            cursor.execute(
                """
                INSERT INTO Orders (OrderNo, ContactID, OrderDate, TotalAmount, PaymentStatus, OrderStatus)
                VALUES (?, ?, datetime('now'), ?, '未支付', '待确认')
                """,
                (new_order_no, 1, new_price),
            )

            db.conn.commit()
            print(f"事务处理成功！创建新订单: {new_order_no}")

        except Exception as e:  # noqa: BLE001
            db.conn.rollback()
            print(f"事务处理失败，已回滚: {str(e)}")

        # 演示4：游标属性使用
        print("\n【演示4：游标属性】")
        _print_cursor_meta(cursor)

    except Exception as e:  # noqa: BLE001
        print(f"游标操作出错: {str(e)}")
    finally:
        if cursor:
            try:
                cursor.close()
                print("\n游标已关闭")
            except Exception:
                print("\n游标关闭时出现问题，但连接会被关闭")
        db.close()


def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 游标操作演示工具          ")
    print("=" * 50)

    while True:
        print("\n游标操作选项:")
        print("1. 执行游标基本操作演示")
        print("2. 退出")

        choice = input("\n请选择操作(1-2): ")

        if choice == "1":
            cursor_basic_operations()
        elif choice == "2":
            break
        else:
            print("无效的选择，请重新输入")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
