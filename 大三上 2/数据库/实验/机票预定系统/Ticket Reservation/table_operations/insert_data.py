"""
实验步骤5: 向表中添加数据
功能: 插入测试数据到各个表中
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists
from datetime import datetime

def insert_test_data():
    """插入测试数据"""
    print("=== 开始插入测试数据 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！请先创建数据库和表结构")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    try:
        # 插入用户数据
        print("\n正在插入用户数据...")
        users = [
            ('admin', 'admin123', '系统管理员', '13800138000', 'admin@airline.com', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('user1', 'user123', '张三', '13900139001', 'zhangsan@example.com', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('user2', 'user456', '李四', '13900139002', 'lisi@example.com', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('user3', 'user789', '王五', '13900139003', 'wangwu@example.com', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ]
        
        user_count = 0
        for user in users:
            if db.execute('''
                INSERT OR IGNORE INTO User (Username, Password, Name, Phone, Email, RegisterTime)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', user):
                user_count += 1
        
        print(f"成功插入 {user_count} 条用户数据")
        
        # 插入乘客数据
        print("\n正在插入乘客数据...")
        passengers = [
            ('张三', '110101199001011234', '13900139001', 'zhangsan@example.com'),
            ('李四', '110101199102022345', '13900139002', 'lisi@example.com'),
            ('王五', '110101199203033456', '13900139003', 'wangwu@example.com'),
            ('赵六', '110101199304044567', '13900139004', 'zhaoliu@example.com'),
            ('孙七', '110101199405055678', '13900139005', 'sunqi@example.com')
        ]
        
        passenger_count = 0
        for passenger in passengers:
            if db.execute('''
                INSERT OR IGNORE INTO Passenger (Name, IDCard, Phone, Email)
                VALUES (?, ?, ?, ?)
            ''', passenger):
                passenger_count += 1
        
        print(f"成功插入 {passenger_count} 条乘客数据")
        
        # 插入航班数据
        print("\n正在插入航班数据...")
        flights = [
            ('CA1234', '中国国际航空', '北京', '上海', '2025-01-01 08:00:00', '2025-01-01 10:30:00', '波音737', 180, 180, 820.0, '正常'),
            ('MU5678', '东方航空', '上海', '广州', '2025-01-01 12:00:00', '2025-01-01 14:30:00', '空客A320', 150, 150, 660.0, '正常'),
            ('CZ3456', '南方航空', '广州', '北京', '2025-01-01 16:00:00', '2025-01-01 18:30:00', '波音787', 250, 250, 980.0, '正常'),
            ('HU7890', '海南航空', '北京', '深圳', '2025-01-02 09:00:00', '2025-01-02 11:45:00', '空客A330', 220, 220, 860.0, '正常'),
            ('ZH4321', '深圳航空', '深圳', '上海', '2025-01-02 14:00:00', '2025-01-02 16:20:00', '波音737', 160, 160, 720.0, '正常'),
            ('PN1022', '西部航空', '成都', '昆明', '2025-01-03 09:40:00', '2025-01-03 11:05:00', '空客A319', 150, 150, 520.0, '正常'),
            ('SC8899', '山东航空', '青岛', '上海', '2025-01-03 13:15:00', '2025-01-03 15:00:00', '波音737', 180, 180, 640.0, '正常'),
            ('FM2335', '上海航空', '上海', '北京', '2025-01-04 07:20:00', '2025-01-04 09:40:00', '波音787', 240, 240, 990.0, '延误'),
            ('MF8765', '厦门航空', '厦门', '杭州', '2025-01-04 12:20:00', '2025-01-04 14:10:00', '波音737', 170, 170, 560.0, '正常'),
            ('3U4556', '四川航空', '重庆', '北京', '2025-01-05 18:30:00', '2025-01-05 21:05:00', '空客A321', 200, 200, 930.0, '正常'),
            ('GS9012', '天津航空', '天津', '西安', '2025-01-06 07:15:00', '2025-01-06 09:20:00', '空客A320', 168, 168, 580.0, '正常'),
            ('EU2233', '成都航空', '成都', '拉萨', '2025-01-06 12:10:00', '2025-01-06 14:30:00', '空客A319', 144, 144, 1020.0, '正常'),
            ('JD7788', '首都航空', '杭州', '三亚', '2025-01-07 09:00:00', '2025-01-07 11:50:00', '空客A321', 200, 200, 880.0, '正常'),
            ('AQ6600', '九元航空', '广州', '南京', '2025-01-07 15:20:00', '2025-01-07 17:35:00', '波音737', 186, 186, 620.0, '正常'),
            ('NS5566', '河北航空', '石家庄', '哈尔滨', '2025-01-08 08:10:00', '2025-01-08 10:45:00', '波音737', 170, 170, 700.0, '正常'),
            ('KY4455', '昆明航空', '昆明', '贵阳', '2025-01-08 13:30:00', '2025-01-08 14:35:00', '波音737', 160, 160, 480.0, '正常'),
            ('DR3344', '瑞丽航空', '长沙', '呼和浩特', '2025-01-09 10:00:00', '2025-01-09 12:35:00', '波音737', 170, 170, 740.0, '正常'),
            ('GJ1122', '长龙航空', '宁波', '厦门', '2025-01-09 16:20:00', '2025-01-09 17:50:00', '波音737', 178, 178, 560.0, '正常'),
            ('8L2040', '祥鹏航空', '昆明', '西双版纳', '2025-01-10 09:45:00', '2025-01-10 10:50:00', '波音737', 156, 156, 420.0, '正常'),
            ('OQ9090', '重庆航空', '重庆', '青岛', '2025-01-10 18:30:00', '2025-01-10 21:05:00', '空客A320', 174, 174, 760.0, '正常')
        ]
        
        flight_count = 0
        for flight in flights:
            if db.execute('''
                INSERT OR IGNORE INTO Flight (FlightNo, Airline, Departure, Destination, DepartureTime, 
                                              ArrivalTime, AircraftType, SeatCount, RemainingSeats, Price, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', flight):
                flight_count += 1
        
        print(f"成功插入 {flight_count} 条航班数据")
        
        # 插入订单数据
        print("\n正在插入订单数据...")
        orders = [
            ('ORD2025001', 2, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1640.0, '已支付', '已确认'),
            ('ORD2025002', 3, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 660.0, '已支付', '已确认'),
            ('ORD2025003', 2, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 980.0, '未支付', '待确认'),
            ('ORD2025004', 4, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 520.0, '未支付', '待确认'),
            ('ORD2025005', 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1860.0, '已支付', '已确认')
        ]
        
        order_count = 0
        for order in orders:
            if db.execute('''
                INSERT OR IGNORE INTO Orders (OrderNo, ContactID, OrderDate, TotalAmount, PaymentStatus, OrderStatus)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', order):
                order_count += 1
        
        print(f"成功插入 {order_count} 条订单数据")
        
        # 插入机票数据
        print("\n正在插入机票数据...")
        tickets = [
            (1, 'A1', 820.0, '经济舱', '有效', 1, 1),
            (1, 'A2', 820.0, '经济舱', '有效', 2, 1),
            (2, 'B1', 660.0, '经济舱', '有效', 3, 2),
            (3, 'C1', 980.0, '商务舱', '有效', 1, 3),
            (4, 'D1', 860.0, '经济舱', '有效', 4, 5),
            (6, 'E1', 520.0, '经济舱', '有效', 5, 4)
        ]
        
        ticket_count = 0
        for ticket in tickets:
            if db.execute('''
                INSERT OR IGNORE INTO Ticket (FlightID, SeatNo, Price, ClassType, Status, PassengerID, OrderID)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ticket):
                ticket_count += 1
        
        print(f"成功插入 {ticket_count} 条机票数据")
        
        print("\n" + "=" * 50)
        print(f"数据插入完成！总计插入:")
        print(f"  用户: {user_count} 条")
        print(f"  乘客: {passenger_count} 条")
        print(f"  航班: {flight_count} 条")
        print(f"  订单: {order_count} 条")
        print(f"  机票: {ticket_count} 条")
        print("=" * 50)
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n插入数据时发生错误: {e}")
        db.close()
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 测试数据插入工具          ")
    print("=" * 50)
    
    # 插入测试数据
    success = insert_test_data()
    
    if success:
        print("\n测试数据插入完成！")
        print("接下来可以执行 query_data.py 查询数据")
    else:
        print("\n测试数据插入失败！")
    
    print("=" * 50)

if __name__ == "__main__":
    main()