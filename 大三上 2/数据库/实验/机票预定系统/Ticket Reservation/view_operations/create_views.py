"""
实验步骤7: 创建视图
功能: 创建各种类型的视图
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists

def create_all_views():
    """创建所有视图"""
    print("=== 开始创建视图 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！请先创建数据库和表结构")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    # 视图创建计划
    views = [
        # 1. 航班信息视图 - 简化的航班信息展示
        {
            'name': 'FlightInfoView',
            'sql': """
                CREATE VIEW IF NOT EXISTS FlightInfoView AS
                SELECT 
                    f.FlightID,
                    f.FlightNo,
                    f.Airline,
                    f.Departure,
                    f.Destination,
                    f.DepartureTime,
                    f.ArrivalTime,
                    f.Price,
                    f.Status,
                    f.RemainingSeats || '/' || f.SeatCount AS SeatAvailability
                FROM Flight f
            """,
            'description': '航班信息视图 - 包含座位可用情况'
        },
        
        # 2. 订单详情视图 - 包含用户信息的订单详情
        {
            'name': 'OrderDetailView',
            'sql': """
                CREATE VIEW IF NOT EXISTS OrderDetailView AS
                SELECT 
                    o.OrderID,
                    o.OrderNo,
                    u.Name AS ContactName,
                    u.Phone AS ContactPhone,
                    o.OrderDate,
                    o.TotalAmount,
                    o.PaymentStatus,
                    o.OrderStatus
                FROM Orders o
                JOIN User u ON o.ContactID = u.UserID
            """,
            'description': '订单详情视图 - 包含联系人信息'
        },
        
        # 3. 机票详情视图 - 完整的机票信息
        {
            'name': 'TicketDetailView',
            'sql': """
                CREATE VIEW IF NOT EXISTS TicketDetailView AS
                SELECT 
                    t.TicketID,
                    f.FlightNo,
                    f.Airline,
                    f.Departure || '->' || f.Destination AS Route,
                    f.DepartureTime,
                    p.Name AS PassengerName,
                    p.IDCard AS PassengerIDCard,
                    t.SeatNo,
                    t.ClassType,
                    t.Price,
                    t.Status,
                    o.OrderNo
                FROM Ticket t
                JOIN Flight f ON t.FlightID = f.FlightID
                JOIN Passenger p ON t.PassengerID = p.PassengerID
                JOIN Orders o ON t.OrderID = o.OrderID
            """,
            'description': '机票详情视图 - 完整的机票信息'
        },
        
        # 4. 用户订单统计视图 - 统计每个用户的订单情况
        {
            'name': 'UserOrderStatsView',
            'sql': """
                CREATE VIEW IF NOT EXISTS UserOrderStatsView AS
                SELECT 
                    u.UserID,
                    u.Username,
                    u.Name,
                    COUNT(o.OrderID) AS TotalOrders,
                    SUM(o.TotalAmount) AS TotalSpent,
                    AVG(o.TotalAmount) AS AvgOrderAmount,
                    MAX(o.OrderDate) AS LastOrderDate
                FROM User u
                LEFT JOIN Orders o ON u.UserID = o.ContactID
                GROUP BY u.UserID, u.Username, u.Name
            """,
            'description': '用户订单统计视图 - 统计用户订单情况'
        },
        
        # 5. 航班上座率视图 - 统计航班的座位销售情况
        {
            'name': 'FlightOccupancyView',
            'sql': """
                CREATE VIEW IF NOT EXISTS FlightOccupancyView AS
                SELECT 
                    f.FlightID,
                    f.FlightNo,
                    f.Airline,
                    f.Departure || '->' || f.Destination AS Route,
                    f.DepartureTime,
                    f.SeatCount,
                    (f.SeatCount - f.RemainingSeats) AS SeatsSold,
                    f.RemainingSeats,
                    ROUND(((f.SeatCount - f.RemainingSeats) * 100.0 / f.SeatCount), 2) AS OccupancyRate,
                    COUNT(t.TicketID) AS TicketsIssued
                FROM Flight f
                LEFT JOIN Ticket t ON f.FlightID = t.FlightID
                GROUP BY f.FlightID, f.FlightNo, f.Airline, f.Departure, f.Destination, 
                         f.DepartureTime, f.SeatCount, f.RemainingSeats
            """,
            'description': '航班上座率视图 - 统计航班座位销售情况'
        },
        
        # 6. 每日航班统计视图 - 按日期统计航班情况
        {
            'name': 'DailyFlightStatsView',
            'sql': """
                CREATE VIEW IF NOT EXISTS DailyFlightStatsView AS
                SELECT 
                    DATE(DepartureTime) AS FlightDate,
                    COUNT(FlightID) AS TotalFlights,
                    SUM(SeatCount) AS TotalSeats,
                    SUM(SeatCount - RemainingSeats) AS SeatsSold,
                    ROUND(AVG(((SeatCount - RemainingSeats) * 100.0 / SeatCount)), 2) AS AvgOccupancyRate
                FROM Flight
                GROUP BY DATE(DepartureTime)
                ORDER BY FlightDate
            """,
            'description': '每日航班统计视图 - 按日期统计航班情况'
        }
    ]
    
    created_views = []
    
    for view in views:
        try:
            if db.execute(view['sql']):
                print(f"✓ {view['name']} - {view['description']}")
                created_views.append(view['name'])
            else:
                print(f"✗ {view['name']} - 创建失败")
                
        except Exception as e:
            print(f"✗ {view['name']} - 错误: {e}")
    
    print(f"\n视图创建完成！成功创建 {len(created_views)} 个视图")
    
    # 显示视图的作用
    print("\n=== 视图的作用和优势 ===")
    print("1. 简化复杂查询，提高开发效率")
    print("2. 数据安全性，隐藏敏感字段")
    print("3. 逻辑数据独立性，表结构变化不影响应用")
    print("4. 数据聚合和统计，便于分析")
    
    db.close()
    return True

def create_specific_view():
    """创建指定视图"""
    print("=== 创建指定视图 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    print("可用的视图创建选项:")
    print("1. 航班信息视图 (FlightInfoView)")
    print("2. 订单详情视图 (OrderDetailView)")
    print("3. 机票详情视图 (TicketDetailView)")
    print("4. 用户订单统计视图 (UserOrderStatsView)")
    print("5. 航班上座率视图 (FlightOccupancyView)")
    print("6. 每日航班统计视图 (DailyFlightStatsView)")
    print("7. 返回")
    
    choice = input("\n请选择要创建的视图(1-7): ")
    
    view_options = {
        '1': {
            'name': 'FlightInfoView',
            'sql': """
                CREATE VIEW IF NOT EXISTS FlightInfoView AS
                SELECT 
                    f.FlightID,
                    f.FlightNo,
                    f.Airline,
                    f.Departure,
                    f.Destination,
                    f.DepartureTime,
                    f.ArrivalTime,
                    f.Price,
                    f.Status,
                    f.RemainingSeats || '/' || f.SeatCount AS SeatAvailability
                FROM Flight f
            """,
            'description': '航班信息视图'
        },
        '2': {
            'name': 'OrderDetailView',
            'sql': """
                CREATE VIEW IF NOT EXISTS OrderDetailView AS
                SELECT 
                    o.OrderID,
                    o.OrderNo,
                    u.Name AS ContactName,
                    u.Phone AS ContactPhone,
                    o.OrderDate,
                    o.TotalAmount,
                    o.PaymentStatus,
                    o.OrderStatus
                FROM Orders o
                JOIN User u ON o.ContactID = u.UserID
            """,
            'description': '订单详情视图'
        },
        '3': {
            'name': 'TicketDetailView',
            'sql': """
                CREATE VIEW IF NOT EXISTS TicketDetailView AS
                SELECT 
                    t.TicketID,
                    f.FlightNo,
                    f.Airline,
                    f.Departure || '->' || f.Destination AS Route,
                    f.DepartureTime,
                    p.Name AS PassengerName,
                    p.IDCard AS PassengerIDCard,
                    t.SeatNo,
                    t.ClassType,
                    t.Price,
                    t.Status,
                    o.OrderNo
                FROM Ticket t
                JOIN Flight f ON t.FlightID = f.FlightID
                JOIN Passenger p ON t.PassengerID = p.PassengerID
                JOIN Orders o ON t.OrderID = o.OrderID
            """,
            'description': '机票详情视图'
        },
        '4': {
            'name': 'UserOrderStatsView',
            'sql': """
                CREATE VIEW IF NOT EXISTS UserOrderStatsView AS
                SELECT 
                    u.UserID,
                    u.Username,
                    u.Name,
                    COUNT(o.OrderID) AS TotalOrders,
                    SUM(o.TotalAmount) AS TotalSpent,
                    AVG(o.TotalAmount) AS AvgOrderAmount,
                    MAX(o.OrderDate) AS LastOrderDate
                FROM User u
                LEFT JOIN Orders o ON u.UserID = o.ContactID
                GROUP BY u.UserID, u.Username, u.Name
            """,
            'description': '用户订单统计视图'
        },
        '5': {
            'name': 'FlightOccupancyView',
            'sql': """
                CREATE VIEW IF NOT EXISTS FlightOccupancyView AS
                SELECT 
                    f.FlightID,
                    f.FlightNo,
                    f.Airline,
                    f.Departure || '->' || f.Destination AS Route,
                    f.DepartureTime,
                    f.SeatCount,
                    (f.SeatCount - f.RemainingSeats) AS SeatsSold,
                    f.RemainingSeats,
                    ROUND(((f.SeatCount - f.RemainingSeats) * 100.0 / f.SeatCount), 2) AS OccupancyRate,
                    COUNT(t.TicketID) AS TicketsIssued
                FROM Flight f
                LEFT JOIN Ticket t ON f.FlightID = t.FlightID
                GROUP BY f.FlightID, f.FlightNo, f.Airline, f.Departure, f.Destination, 
                         f.DepartureTime, f.SeatCount, f.RemainingSeats
            """,
            'description': '航班上座率视图'
        },
        '6': {
            'name': 'DailyFlightStatsView',
            'sql': """
                CREATE VIEW IF NOT EXISTS DailyFlightStatsView AS
                SELECT 
                    DATE(DepartureTime) AS FlightDate,
                    COUNT(FlightID) AS TotalFlights,
                    SUM(SeatCount) AS TotalSeats,
                    SUM(SeatCount - RemainingSeats) AS SeatsSold,
                    ROUND(AVG(((SeatCount - RemainingSeats) * 100.0 / SeatCount)), 2) AS AvgOccupancyRate
                FROM Flight
                GROUP BY DATE(DepartureTime)
                ORDER BY FlightDate
            """,
            'description': '每日航班统计视图'
        }
    }
    
    if choice in view_options and choice != '7':
        view = view_options[choice]
        
        print(f"\n创建视图: {view['name']}")
        print(f"描述: {view['description']}")
        
        confirm = input("\n确认创建此视图？(y/n): ").lower()
        if confirm == 'y':
            if db.execute(view['sql']):
                print(f"✓ 视图 {view['name']} 创建成功！")
            else:
                print(f"✗ 视图 {view['name']} 创建失败！")
    
    elif choice == '7':
        pass
    else:
        print("无效的选择")
    
    db.close()
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 视图创建工具          ")
    print("=" * 50)
    
    while True:
        print("\n视图创建选项:")
        print("1. 创建所有推荐视图")
        print("2. 创建指定视图")
        print("3. 查看现有视图")
        print("4. 退出")
        
        choice = input("\n请选择操作(1-4): ")
        
        if choice == '1':
            create_all_views()
        elif choice == '2':
            create_specific_view()
        elif choice == '3':
            # 查看现有视图
            if database_exists():
                db = DatabaseManager()
                if db.connect():
                    views = db.fetch_all("SELECT name, sql FROM sqlite_master WHERE type='view'")
                    if views:
                        print(f"\n当前数据库中的视图 ({len(views)} 个):")
                        for view in views:
                            print(f"\n名称: {view[0]}")
                            print(f"定义: {view[1]}")
                    else:
                        print("\n没有找到任何视图")
                    db.close()
                else:
                    print("无法连接到数据库")
            else:
                print("数据库不存在")
        elif choice == '4':
            break
        else:
            print("无效的选择，请重新输入")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()