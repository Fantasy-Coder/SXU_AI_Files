"""
实验步骤1: 创建数据库
功能: 创建SQLite数据库文件和初始配置
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists

def create_database(db_name='airline_ticket_system.db'):
    """创建数据库"""
    print("=== 开始创建数据库 ===")
    
    # 检查数据库是否已存在
    if database_exists(db_name):
        print(f"警告: 数据库 {db_name} 已存在！")
        choice = input("是否要覆盖现有数据库？(y/n): ").lower()
        if choice != 'y':
            print("取消创建数据库")
            return False
    
    try:
        # 创建数据库连接（如果不存在会自动创建）
        db = DatabaseManager(db_name)
        if db.connect():
            print(f"数据库 {db_name} 创建成功！")
            
            # 获取数据库信息
            db_info = db.get_database_info()
            print(f"\n数据库初始信息:")
            print(f"表数量: {len(db_info['tables'])}")
            print(f"索引数量: {len(db_info['indexes'])}")
            print(f"视图数量: {len(db_info['views'])}")
            
            db.close()
            return True
        else:
            print(f"数据库 {db_name} 创建失败！")
            return False
    
    except Exception as e:
        print(f"创建数据库时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 数据库创建工具          ")
    print("=" * 50)
    
    # 创建数据库
    success = create_database()
    
    if success:
        print("\n数据库创建完成！")
        print("接下来可以执行 create_tables.py 来创建表结构")
    else:
        print("\n数据库创建失败！")
    
    print("=" * 50)

if __name__ == "__main__":
    main()