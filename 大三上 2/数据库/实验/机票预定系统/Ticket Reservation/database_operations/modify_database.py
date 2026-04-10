"""
实验步骤2: 修改数据库
功能: 修改数据库配置、备份、恢复等操作
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists, backup_database, restore_database
from datetime import datetime

def modify_database_config(db_name='airline_ticket_system.db'):
    """修改数据库配置"""
    print("=== 修改数据库配置 ===")
    
    if not database_exists(db_name):
        print(f"错误: 数据库 {db_name} 不存在！")
        return False
    
    db = DatabaseManager(db_name)
    if not db.connect():
        return False
    
    print("\n当前数据库配置:")
    print("1. 外键约束: 已启用")
    print("2. 数据库编码: UTF-8")
    print("3. 页面大小: 4096 bytes")
    print("4. 缓存大小: 2000 pages")
    
    # SQLite的配置修改比较有限，主要通过PRAGMA语句
    print("\n可修改的配置选项:")
    print("1. 缓存大小")
    print("2. 同步模式")
    print("3. 数据库编码")
    print("4. 退出")
    
    while True:
        choice = input("\n请选择要修改的配置(1-4): ")
        
        if choice == '1':
            cache_size = input("请输入新的缓存大小(页数，默认2000): ")
            if cache_size.isdigit():
                if db.execute(f"PRAGMA cache_size = {cache_size}"):
                    print(f"缓存大小已设置为 {cache_size} 页")
                else:
                    print("设置缓存大小失败")
        
        elif choice == '2':
            print("同步模式选项:")
            print("0 - OFF (最快，不安全)")
            print("1 - NORMAL (默认)")
            print("2 - FULL (最安全，最慢)")
            sync_mode = input("请选择同步模式(0-2): ")
            if sync_mode in ['0', '1', '2']:
                if db.execute(f"PRAGMA synchronous = {sync_mode}"):
                    print(f"同步模式已设置为 {sync_mode}")
                else:
                    print("设置同步模式失败")
        
        elif choice == '3':
            encoding = input("请输入新的数据库编码(默认UTF-8): ")
            if encoding:
                if db.execute(f"PRAGMA encoding = '{encoding}'"):
                    print(f"数据库编码已设置为 {encoding}")
                else:
                    print("设置数据库编码失败")
        
        elif choice == '4':
            break
        
        else:
            print("无效的选择，请重新输入")
    
    db.close()
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 数据库修改工具          ")
    print("=" * 50)
    
    if not database_exists():
        print("错误: 数据库不存在！请先创建数据库")
        print("=" * 50)
        return
    
    print("\n数据库修改选项:")
    print("1. 修改数据库配置")
    print("2. 备份数据库")
    print("3. 恢复数据库")
    print("4. 查看数据库信息")
    print("5. 退出")
    
    while True:
        choice = input("\n请选择操作(1-5): ")
        
        if choice == '1':
            modify_database_config()
        
        elif choice == '2':
            backup_name = input("请输入备份文件名(按回车使用默认名称): ")
            if backup_database(backup_name=backup_name if backup_name else None):
                print("备份成功！")
            else:
                print("备份失败！")
        
        elif choice == '3':
            backup_file = input("请输入要恢复的备份文件名: ")
            if os.path.exists(backup_file):
                if restore_database(backup_file):
                    print("恢复成功！")
                else:
                    print("恢复失败！")
            else:
                print(f"错误: 备份文件 {backup_file} 不存在！")
        
        elif choice == '4':
            db = DatabaseManager()
            if db.connect():
                db_info = db.get_database_info()
                print("\n数据库详细信息:")
                print(f"数据库文件: airline_ticket_system.db")
                print(f"创建时间: {datetime.fromtimestamp(os.path.getctime('airline_ticket_system.db'))}")
                print(f"最后修改时间: {datetime.fromtimestamp(os.path.getmtime('airline_ticket_system.db'))}")
                print(f"文件大小: {os.path.getsize('airline_ticket_system.db')} bytes")
                print(f"\n对象统计:")
                print(f"表: {len(db_info['tables'])} 个")
                print(f"索引: {len(db_info['indexes'])} 个")
                print(f"视图: {len(db_info['views'])} 个")
                
                if db_info['tables']:
                    print(f"\n表列表:")
                    for table in db_info['tables']:
                        schema = db.get_table_schema(table)
                        print(f"  - {table} ({len(schema)} 个字段)")
                
                db.close()
            else:
                print("无法连接到数据库！")
        
        elif choice == '5':
            break
        
        else:
            print("无效的选择，请重新输入")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()