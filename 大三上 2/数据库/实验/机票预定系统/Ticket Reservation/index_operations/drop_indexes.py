"""
实验步骤9: 删除索引
功能: 删除索引
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists

def drop_all_indexes():
    """删除所有索引"""
    print("=== 开始删除所有索引 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    print("警告: 你即将删除所有索引！")
    print("此操作将删除所有自定义索引，但不会影响表结构和数据")
    
    # 安全确认
    confirm = input("请输入 'DROP' 确认删除: ")
    if confirm != 'DROP':
        print("取消删除操作")
        db.close()
        return False
    
    try:
        # 获取所有索引
        indexes = db.fetch_all("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
        
        if not indexes:
            print("没有找到可删除的索引")
            db.close()
            return True
        
        print(f"\n找到 {len(indexes)} 个索引:")
        for index in indexes:
            print(f"  - {index[0]}")
        
        # 逐个删除索引
        drop_count = 0
        for index in indexes:
            index_name = index[0]
            if db.execute(f"DROP INDEX IF EXISTS {index_name}"):
                print(f"  索引 {index_name} 删除成功")
                drop_count += 1
            else:
                print(f"  索引 {index_name} 删除失败")
        
        print(f"\n成功删除 {drop_count} 个索引")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n删除索引时发生错误: {e}")
        db.close()
        return False

def drop_specific_index():
    """删除指定索引"""
    print("=== 删除指定索引 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    # 获取所有索引
    indexes = db.fetch_all("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    
    if not indexes:
        print("没有找到可删除的索引")
        db.close()
        return True
    
    print("当前数据库中的索引:")
    for i, index in enumerate(indexes, 1):
        print(f"  {i}. {index[0]} (表: {index[1]})")
    
    choice = input("\n请选择要删除的索引编号(0取消): ")
    if choice == '0':
        print("取消删除操作")
        db.close()
        return True
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(indexes):
            index_name = indexes[index][0]
            table_name = indexes[index][1]
            
            print(f"\n警告: 你即将删除索引 {index_name} (表: {table_name})！")
            confirm = input("请输入 'DROP' 确认删除: ")
            if confirm != 'DROP':
                print("取消删除操作")
                db.close()
                return True
            
            if db.execute(f"DROP INDEX IF EXISTS {index_name}"):
                print(f"索引 {index_name} 删除成功！")
            else:
                print(f"索引 {index_name} 删除失败！")
        else:
            print("无效的选择")
    
    except ValueError:
        print("请输入有效的数字")
    
    db.close()
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 索引删除工具          ")
    print("=" * 50)
    
    while True:
        print("\n删除选项:")
        print("1. 删除所有索引")
        print("2. 删除指定索引")
        print("3. 查看索引信息")
        print("4. 退出")
        
        choice = input("\n请选择操作(1-4): ")
        
        if choice == '1':
            drop_all_indexes()
        elif choice == '2':
            drop_specific_index()
        elif choice == '3':
            # 查看索引详细信息
            if database_exists():
                db = DatabaseManager()
                if db.connect():
                    indexes = db.fetch_all("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'")
                    if indexes:
                        print(f"\n索引详细信息 ({len(indexes)} 个):")
                        for idx in indexes:
                            print(f"\n名称: {idx[0]}")
                            print(f"表名: {idx[1]}")
                            print(f"定义: {idx[2]}")
                    else:
                        print("\n没有找到任何索引")
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