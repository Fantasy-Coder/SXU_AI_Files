"""
实验步骤9: 删除视图
功能: 删除视图
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists

def drop_all_views():
    """删除所有视图"""
    print("=== 开始删除所有视图 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    print("警告: 你即将删除所有视图！")
    print("此操作将删除所有自定义视图，但不会影响表结构和数据")
    
    # 安全确认
    confirm = input("请输入 'DROP' 确认删除: ")
    if confirm != 'DROP':
        print("取消删除操作")
        db.close()
        return False
    
    try:
        # 获取所有视图
        views = db.fetch_all("SELECT name FROM sqlite_master WHERE type='view'")
        
        if not views:
            print("没有找到可删除的视图")
            db.close()
            return True
        
        print(f"\n找到 {len(views)} 个视图:")
        for view in views:
            print(f"  - {view[0]}")
        
        # 逐个删除视图
        drop_count = 0
        for view in views:
            view_name = view[0]
            if db.execute(f"DROP VIEW IF EXISTS {view_name}"):
                print(f"  视图 {view_name} 删除成功")
                drop_count += 1
            else:
                print(f"  视图 {view_name} 删除失败")
        
        print(f"\n成功删除 {drop_count} 个视图")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n删除视图时发生错误: {e}")
        db.close()
        return False

def drop_specific_view():
    """删除指定视图"""
    print("=== 删除指定视图 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    # 获取所有视图
    views = db.fetch_all("SELECT name FROM sqlite_master WHERE type='view'")
    
    if not views:
        print("没有找到可删除的视图")
        db.close()
        return True
    
    print("当前数据库中的视图:")
    for i, view in enumerate(views, 1):
        print(f"  {i}. {view[0]}")
    
    choice = input("\n请选择要删除的视图编号(0取消): ")
    if choice == '0':
        print("取消删除操作")
        db.close()
        return True
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(views):
            view_name = views[index][0]
            
            print(f"\n警告: 你即将删除视图 {view_name}！")
            confirm = input("请输入 'DROP' 确认删除: ")
            if confirm != 'DROP':
                print("取消删除操作")
                db.close()
                return True
            
            if db.execute(f"DROP VIEW IF EXISTS {view_name}"):
                print(f"视图 {view_name} 删除成功！")
            else:
                print(f"视图 {view_name} 删除失败！")
        else:
            print("无效的选择")
    
    except ValueError:
        print("请输入有效的数字")
    
    db.close()
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 视图删除工具          ")
    print("=" * 50)
    
    while True:
        print("\n删除选项:")
        print("1. 删除所有视图")
        print("2. 删除指定视图")
        print("3. 查看视图信息")
        print("4. 退出")
        
        choice = input("\n请选择操作(1-4): ")
        
        if choice == '1':
            drop_all_views()
        elif choice == '2':
            drop_specific_view()
        elif choice == '3':
            # 查看视图详细信息
            if database_exists():
                db = DatabaseManager()
                if db.connect():
                    views = db.fetch_all("SELECT name, sql FROM sqlite_master WHERE type='view'")
                    if views:
                        print(f"\n视图详细信息 ({len(views)} 个):")
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