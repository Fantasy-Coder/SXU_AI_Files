"""
实验步骤3: 删除数据库
功能: 删除SQLite数据库文件
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import database_exists, backup_database

def drop_database(db_name='airline_ticket_system.db'):
    """删除数据库"""
    print("=== 开始删除数据库 ===")
    
    # 检查数据库是否存在
    if not database_exists(db_name):
        print(f"错误: 数据库 {db_name} 不存在！")
        return False
    
    print(f"警告: 你即将删除数据库 {db_name}！")
    print("此操作将永久删除所有数据，无法恢复！")
    
    # 安全确认
    confirm = input("请输入 'DELETE' 确认删除: ")
    if confirm != 'DELETE':
        print("取消删除操作")
        return False
    
    # 提供备份选项
    backup_choice = input("是否要先备份数据库？(y/n): ").lower()
    if backup_choice == 'y':
        print("\n正在创建数据库备份...")
        if backup_database(db_name):
            print("数据库备份成功！")
        else:
            print("数据库备份失败，是否继续删除？")
            continue_choice = input("(y/n): ").lower()
            if continue_choice != 'y':
                print("取消删除操作")
                return False
    
    try:
        # 尝试删除数据库文件
        os.remove(db_name)
        print(f"\n数据库 {db_name} 删除成功！")
        return True
    
    except Exception as e:
        print(f"\n删除数据库时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 数据库删除工具          ")
    print("=" * 50)
    print("⚠️  警告: 此工具将永久删除数据库文件 ⚠️")
    print("=" * 50)
    
    # 执行删除操作
    success = drop_database()
    
    if success:
        print("\n数据库已成功删除！")
        print("需要重新创建数据库，请运行 create_database.py")
    else:
        print("\n数据库删除操作已取消或失败！")
    
    print("=" * 50)

if __name__ == "__main__":
    main()