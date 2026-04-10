"""
实验步骤7: 查询视图
功能: 查询视图数据、通过视图修改数据
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists
from prettytable import PrettyTable

def display_view_data(view_name, data, headers):
    """显示视图数据"""
    if not data:
        print(f"视图 {view_name} 中没有数据")
        return
    
    table = PrettyTable()
    table.field_names = headers
    
    for row in data:
        table.add_row(row)
    
    print(f"\n视图 {view_name} 数据:")
    print(table)

def query_flight_info_view(db):
    """查询航班信息视图"""
    print("\n=== 查询航班信息视图 (FlightInfoView) ===")
    
    # 查询所有航班信息
    flights = db.fetch_all("SELECT * FROM FlightInfoView")
    headers = ["航班ID", "航班号", "航空公司", "出发地", "目的地", "出发时间", 
               "到达时间", "票价", "状态", "座位情况"]
    display_view_data("FlightInfoView", flights, headers)
    
    # 通过视图进行条件查询
    print("\n=== 通过视图进行条件查询 ===")
    departure = input("请输入出发地: ")
    destination = input("请输入目的地: ")
    
    flights = db.fetch_all("""
        SELECT FlightNo, Airline, DepartureTime, Price, SeatAvailability 
        FROM FlightInfoView 
        WHERE Departure = ? AND Destination = ?
        ORDER BY DepartureTime
    """, (departure, destination))
    
    headers = ["航班号", "航空公司", "出发时间", "票价", "座位情况"]
    display_view_data(f"{departure}->{destination} 航班", flights, headers)

def query_order_detail_view(db):
    """查询订单详情视图"""
    print("\n=== 查询订单详情视图 (OrderDetailView) ===")
    
    orders = db.fetch_all("SELECT * FROM OrderDetailView")
    headers = ["订单ID", "订单号", "联系人", "联系电话", "订单日期", "总金额", "支付状态", "订单状态"]
    display_view_data("OrderDetailView", orders, headers)

def query_ticket_detail_view(db):
    """查询机票详情视图"""
    print("\n=== 查询机票详情视图 (TicketDetailView) ===")
    
    tickets = db.fetch_all("SELECT * FROM TicketDetailView")
    headers = ["机票ID", "航班号", "航空公司", "航线", "出发时间", "乘客姓名", 
               "身份证号", "座位号", "舱位", "票价", "状态", "订单号"]
    display_view_data("TicketDetailView", tickets, headers)

def query_user_order_stats_view(db):
    """查询用户订单统计视图"""
    print("\n=== 查询用户订单统计视图 (UserOrderStatsView) ===")
    
    stats = db.fetch_all("SELECT * FROM UserOrderStatsView")
    headers = ["用户ID", "用户名", "姓名", "订单总数", "总消费", "平均订单金额", "最后订单日期"]
    display_view_data("UserOrderStatsView", stats, headers)

def query_flight_occupancy_view(db):
    """查询航班上座率视图"""
    print("\n=== 查询航班上座率视图 (FlightOccupancyView) ===")
    
    occupancy = db.fetch_all("""
        SELECT FlightNo, Airline, Route, DepartureTime, SeatCount, SeatsSold, 
               RemainingSeats, OccupancyRate 
        FROM FlightOccupancyView
        ORDER BY OccupancyRate DESC
    """)
    
    headers = ["航班号", "航空公司", "航线", "出发时间", "总座位", "已售座位", "剩余座位", "上座率(%)"]
    display_view_data("FlightOccupancyView", occupancy, headers)

def query_daily_flight_stats_view(db):
    """查询每日航班统计视图"""
    print("\n=== 查询每日航班统计视图 (DailyFlightStatsView) ===")
    
    stats = db.fetch_all("SELECT * FROM DailyFlightStatsView")
    headers = ["航班日期", "航班总数", "总座位数", "已售座位", "平均上座率(%)"]
    display_view_data("DailyFlightStatsView", stats, headers)

def update_through_view(db):
    """通过视图修改数据"""
    print("\n=== 通过视图修改数据 ===")
    print("注意: SQLite 中的视图默认是只读的，无法直接修改")
    print("如果需要通过视图修改数据，需要创建可更新视图")
    
    # 示例：创建可更新视图并进行修改
    print("\n=== 创建可更新视图示例 ===")
    
    # 创建可更新视图
    db.execute("""
        CREATE VIEW IF NOT EXISTS UpdatableFlightView AS
        SELECT FlightID, FlightNo, Status 
        FROM Flight
    """)
    
    # 尝试通过视图修改数据
    flight_id = input("请输入要修改状态的航班ID: ")
    new_status = input("请输入新的航班状态(正常/延误/取消): ")
    
    # 在SQLite中，即使是简单视图也可能无法更新
    # 这里我们直接更新基表
    if db.execute("""
        UPDATE Flight 
        SET Status = ? 
        WHERE FlightID = ?
    """, (new_status, flight_id)):
        print("航班状态修改成功！")
    else:
        print("航班状态修改失败！")

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 视图查询和操作工具          ")
    print("=" * 50)
    
    if not database_exists():
        print("错误: 数据库不存在！请先创建数据库、表结构和视图")
        print("=" * 50)
        return
    
    db = DatabaseManager()
    if not db.connect():
        print("=" * 50)
        return
    
    while True:
        print("\n视图查询选项:")
        print("1. 查询航班信息视图")
        print("2. 查询订单详情视图")
        print("3. 查询机票详情视图")
        print("4. 查询用户订单统计视图")
        print("5. 查询航班上座率视图")
        print("6. 查询每日航班统计视图")
        print("7. 通过视图修改数据")
        print("8. 查看所有视图")
        print("9. 退出")
        
        choice = input("\n请选择查询类型(1-9): ")
        
        if choice == '1':
            query_flight_info_view(db)
        elif choice == '2':
            query_order_detail_view(db)
        elif choice == '3':
            query_ticket_detail_view(db)
        elif choice == '4':
            query_user_order_stats_view(db)
        elif choice == '5':
            query_flight_occupancy_view(db)
        elif choice == '6':
            query_daily_flight_stats_view(db)
        elif choice == '7':
            update_through_view(db)
        elif choice == '8':
            # 查看所有视图
            views = db.fetch_all("SELECT name FROM sqlite_master WHERE type='view'")
            if views:
                print(f"\n当前数据库中的视图 ({len(views)} 个):")
                for view in views:
                    print(f"  - {view[0]}")
            else:
                print("\n没有找到任何视图")
        elif choice == '9':
            break
        else:
            print("无效的选择，请重新输入")
    
    db.close()
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()