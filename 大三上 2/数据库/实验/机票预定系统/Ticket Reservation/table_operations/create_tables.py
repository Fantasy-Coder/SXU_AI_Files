"""
实验步骤4: 创建表
功能: 创建所有需要的表结构
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists

def create_all_tables():
    """创建所有表结构"""
    print("=== 开始创建表结构 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！请先运行 create_database.py 创建数据库")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    # 拆分成单个表的创建语句，避免一次性执行多条SQL
    create_table_sqls = [
        # 用户表
        """
        CREATE TABLE IF NOT EXISTS User (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            Salt TEXT,
            FailedAttempts INTEGER NOT NULL DEFAULT 0,
            LockedUntil TEXT,
            Name TEXT NOT NULL,
            Phone TEXT,
            Email TEXT,
            RegisterTime TEXT NOT NULL
        );
        """,
        # 乘客表
        """
        CREATE TABLE IF NOT EXISTS Passenger (
            PassengerID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            IDCard TEXT NOT NULL UNIQUE,
            Phone TEXT,
            Email TEXT
        );
        """,
        # 航班表
        """
        CREATE TABLE IF NOT EXISTS Flight (
            FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightNo TEXT NOT NULL UNIQUE,
            Airline TEXT NOT NULL,
            Departure TEXT NOT NULL,
            Destination TEXT NOT NULL,
            DepartureTime TEXT NOT NULL,
            ArrivalTime TEXT NOT NULL,
            AircraftType TEXT NOT NULL,
            SeatCount INTEGER NOT NULL CHECK(SeatCount > 0),
            RemainingSeats INTEGER NOT NULL CHECK(RemainingSeats >= 0 AND RemainingSeats <= SeatCount),
            Price REAL NOT NULL CHECK(Price >= 0),
            Status TEXT NOT NULL DEFAULT '未起飞' CHECK(Status IN ('未起飞','已起飞','已降落','取消')),
            CHECK (datetime(ArrivalTime) >= datetime(DepartureTime))
        );
        """,
        # 订单表（使用Orders避免关键字冲突）
        """
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderNo TEXT NOT NULL UNIQUE,
            ContactID INTEGER NOT NULL,
            OrderDate TEXT NOT NULL CHECK(datetime(OrderDate) <= datetime('now','+1 day')),
            TotalAmount REAL NOT NULL CHECK(TotalAmount >= 0),
            PaymentStatus TEXT NOT NULL DEFAULT '未支付' CHECK(PaymentStatus IN ('未支付','已支付','退款中','已退款')),
            OrderStatus TEXT NOT NULL DEFAULT '待确认' CHECK(OrderStatus IN ('待确认','已确认','已取消')),
            FOREIGN KEY (ContactID) REFERENCES User(UserID)
        );
        """,
        # 机票表
        """
        CREATE TABLE IF NOT EXISTS Ticket (
            TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightID INTEGER NOT NULL,
            SeatNo TEXT NOT NULL,
            Price REAL NOT NULL CHECK(Price >= 0),
            ClassType TEXT NOT NULL,
            Status TEXT NOT NULL DEFAULT '有效' CHECK(Status IN ('有效','已退票','已改签')),
            PassengerID INTEGER NOT NULL,
            OrderID INTEGER NOT NULL,
            FOREIGN KEY (FlightID) REFERENCES Flight(FlightID),
            FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
            UNIQUE (FlightID, SeatNo)
        );
        """
    ]
    
    # 逐个执行建表语句
    table_names = ["User", "Passenger", "Flight", "Orders", "Ticket"]
    success_count = 0
    
    try:
        for idx, sql in enumerate(create_table_sqls):
            table = table_names[idx]
            try:
                db.cursor.execute(sql.strip())  # 执行单个表的创建语句
                db.conn.commit()
                print(f"成功创建表：{table}")
                success_count += 1
            except Exception as e:
                print(f"创建表 {table} 失败：{str(e)}")
                # 继续创建其他表，不中断整体流程
                db.conn.rollback()
        
        if success_count == len(table_names):
            print("\n所有表结构创建成功！")
        else:
            print(f"\n部分表创建失败（成功 {success_count}/{len(table_names)} 个）")
            db.close()
            return False
    
    except Exception as e:
        print(f"\n建表过程异常：{str(e)}")
        db.close()
        return False
    
    # 获取创建的表信息并显示
    try:
        # 查询所有表（SQLite原生语法）
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [table[0] for table in db.cursor.fetchall()]
        
        print(f"\n数据库中存在的表数量: {len(tables)}")
        print("创建的表列表:")
        
        for table in tables:
            # 获取表结构
            try:
                db.cursor.execute(f"PRAGMA table_info({table})")
                schema = db.cursor.fetchall()
                
                field_count = len(schema) if schema else 0
                print(f"  - {table}: {field_count} 个字段")
                
                # 可选：显示表结构详情
                show_schema = input(f"  是否显示 {table} 表的详细结构？(y/n，默认n): ").lower()
                if show_schema == 'y':
                    print(f"    {table} 表详细结构：")
                    for field in schema:
                        # field结构：(cid, 字段名, 类型, 是否非空, 默认值, 是否主键)
                        cid, field_name, field_type, not_null, dflt_val, is_pk = field
                        pk_str = "是" if is_pk == 1 else "否"
                        not_null_str = "非空" if not_null == 1 else "可空"
                        default_str = dflt_val if dflt_val is not None else "无"
                        print(f"      - 字段名：{field_name:12} 类型：{field_type:10} 主键：{pk_str:6} 非空：{not_null_str:6} 默认值：{default_str}")
            
            except Exception as e:
                print(f"  - {table}: 获取表结构失败 - {str(e)}")
        
    except Exception as e:
        print(f"\n获取表信息时出错：{str(e)}")
    
    db.close()
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("          机票预订系统 - 表结构创建工具          ")
    print("=" * 60)
    
    # 创建所有表
    success = create_all_tables()
    
    if success:
        print("\n表结构创建流程完成！")
        print("下一步：执行 insert_data.py 插入测试数据")
    else:
        print("\n表结构创建流程失败！")
    
    print("=" * 60)

if __name__ == "__main__":
    main()