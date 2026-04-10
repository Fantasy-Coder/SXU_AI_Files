"""
实验步骤5 & 8: 查询和更新数据
功能: 查询数据、修改数据、各类查询操作
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists
from prettytable import PrettyTable

def display_table_data(table_name, data, headers):
    """显示表格数据"""
    if not data:
        print(f"没有找到 {table_name} 表的数据")
        return
    
    table = PrettyTable()
    table.field_names = headers
    
    for row in data:
        table.add_row(row)
    
    print(f"\n{table_name} 表数据:")
    print(table)

def query_users(db):
    """查询用户数据"""
    print("\n=== 查询用户数据 ===")
    
    # 查询所有用户
    users = db.fetch_all("SELECT UserID, Username, Name, Phone, Email, RegisterTime FROM User")
    headers = ["用户ID", "用户名", "姓名", "电话", "邮箱", "注册时间"]
    display_table_data("User", users, headers)
    
    # 条件查询示例
    print("\n=== 条件查询示例 ===")
    username = input("请输入要查询的用户名: ")
    user = db.fetch_one("SELECT * FROM User WHERE Username = ?", (username,))
    
    if user:
        print(f"\n用户 {username} 的详细信息:")
        print(f"用户ID: {user[0]}")
        print(f"用户名: {user[1]}")
        print(f"姓名: {user[3]}")
        print(f"电话: {user[4]}")
        print(f"邮箱: {user[5]}")
        print(f"注册时间: {user[6]}")
    else:
        print(f"没有找到用户 {username}")

def query_passengers(db):
    """查询乘客数据"""
    print("\n=== 查询乘客数据 ===")
    
    passengers = db.fetch_all("SELECT * FROM Passenger")
    headers = ["乘客ID", "姓名", "身份证号", "电话", "邮箱"]
    display_table_data("Passenger", passengers, headers)

def query_flights(db):
    """查询航班数据"""
    print("\n=== 查询航班数据 ===")
    
    # 所有航班
    flights = db.fetch_all("SELECT * FROM Flight")
    headers = ["航班ID", "航班号", "航空公司", "出发地", "目的地", "出发时间", 
               "到达时间", "机型", "座位总数", "剩余座位", "票价", "状态"]
    display_table_data("Flight", flights, headers)
    
    # 高级查询示例
    print("\n=== 高级查询示例 ===")
    print("1. 查询特定航线的航班")
    print("2. 查询特定航空公司的航班")
    print("3. 查询价格区间内的航班")
    
    choice = input("请选择查询类型(1-3): ")
    
    if choice == '1':
        departure = input("请输入出发地: ")
        destination = input("请输入目的地: ")
        航线_flights = db.fetch_all("""
            SELECT FlightNo, Airline, DepartureTime, Price 
            FROM Flight 
            WHERE Departure = ? AND Destination = ?
        """, (departure, destination))
        headers = ["航班号", "航空公司", "出发时间", "票价"]
        display_table_data(f"{departure}->{destination} 航班", 航线_flights, headers)
    
    elif choice == '2':
        airline = input("请输入航空公司名称: ")
        airline_flights = db.fetch_all("""
            SELECT FlightNo, Departure, Destination, DepartureTime, Price 
            FROM Flight 
            WHERE Airline LIKE ?
        """, (f'%{airline}%',))
        headers = ["航班号", "出发地", "目的地", "出发时间", "票价"]
        display_table_data(f"{airline} 航班", airline_flights, headers)
    
    elif choice == '3':
        min_price = float(input("请输入最低价格: "))
        max_price = float(input("请输入最高价格: "))
        price_flights = db.fetch_all("""
            SELECT FlightNo, Airline, Departure, Destination, Price 
            FROM Flight 
            WHERE Price BETWEEN ? AND ?
            ORDER BY Price ASC
        """, (min_price, max_price))
        headers = ["航班号", "航空公司", "出发地", "目的地", "票价"]
        display_table_data(f"价格区间 {min_price}-{max_price} 航班", price_flights, headers)

def query_orders(db):
    """查询订单数据"""
    print("\n=== 查询订单数据 ===")
    
    # 连接查询示例：订单 + 用户信息
    orders = db.fetch_all("""
        SELECT o.OrderID, o.OrderNo, u.Name AS ContactName, o.OrderDate, o.TotalAmount, o.PaymentStatus, o.OrderStatus
        FROM Orders o
        JOIN User u ON o.ContactID = u.UserID
    """)
    headers = ["订单ID", "订单号", "联系人", "订单日期", "总金额", "支付状态", "订单状态"]
    display_table_data("Orders", orders, headers)

def query_tickets(db):
    """查询机票数据"""
    print("\n=== 查询机票数据 ===")
    
    # 多表连接查询
    tickets = db.fetch_all("""
        SELECT t.TicketID, f.FlightNo, p.Name AS PassengerName, t.SeatNo, t.Price, t.ClassType, t.Status
        FROM Ticket t
        JOIN Flight f ON t.FlightID = f.FlightID
        JOIN Passenger p ON t.PassengerID = p.PassengerID
    """)
    headers = ["机票ID", "航班号", "乘客姓名", "座位号", "票价", "舱位等级", "状态"]
    display_table_data("Ticket", tickets, headers)

def modify_data(db):
    """修改数据"""
    print("\n=== 修改数据 ===")
    print("1. 修改用户信息")
    print("2. 修改航班状态")
    print("3. 修改订单状态")
    print("4. 返回")
    
    choice = input("请选择要修改的数据类型(1-4): ")
    
    if choice == '1':
        # 修改用户信息
        user_id = input("请输入要修改的用户ID: ")
        new_phone = input("请输入新的电话号码: ")
        new_email = input("请输入新的邮箱地址: ")
        
        if db.execute("""
            UPDATE User 
            SET Phone = ?, Email = ? 
            WHERE UserID = ?
        """, (new_phone, new_email, user_id)):
            print("用户信息修改成功！")
        else:
            print("用户信息修改失败！")
    
    elif choice == '2':
        # 修改航班状态
        flight_id = input("请输入要修改的航班ID: ")
        new_status = input("请输入新的航班状态(正常/延误/取消): ")
        
        if db.execute("""
            UPDATE Flight 
            SET Status = ? 
            WHERE FlightID = ?
        """, (new_status, flight_id)):
            print("航班状态修改成功！")
        else:
            print("航班状态修改失败！")
    
    elif choice == '3':
        # 修改订单状态
        order_id = input("请输入要修改的订单ID: ")
        new_status = input("请输入新的订单状态(待确认/已确认/已取消): ")
        
        if db.execute("""
            UPDATE Orders 
            SET OrderStatus = ? 
            WHERE OrderID = ?
        """, (new_status, order_id)):
            print("订单状态修改成功！")
        else:
            print("订单状态修改失败！")

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 数据查询和修改工具          ")
    print("=" * 50)
    
    if not database_exists():
        print("错误: 数据库不存在！请先创建数据库和表结构")
        print("=" * 50)
        return
    
    db = DatabaseManager()
    if not db.connect():
        print("=" * 50)
        return
    
    while True:
        print("\n查询选项:")
        print("1. 查询用户数据")
        print("2. 查询乘客数据")
        print("3. 查询航班数据")
        print("4. 查询订单数据")
        print("5. 查询机票数据")
        print("6. 修改数据")
        print("7. 退出")
        
        choice = input("\n请选择查询类型(1-7): ")
        
        if choice == '1':
            query_users(db)
        elif choice == '2':
            query_passengers(db)
        elif choice == '3':
            query_flights(db)
        elif choice == '4':
            query_orders(db)
        elif choice == '5':
            query_tickets(db)
        elif choice == '6':
            modify_data(db)
        elif choice == '7':
            break
        else:
            print("无效的选择，请重新输入")
    
    db.close()
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()