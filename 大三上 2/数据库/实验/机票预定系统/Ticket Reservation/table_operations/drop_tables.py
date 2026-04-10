"""
实验步骤9: 删除表
功能: 删除表结构
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import DatabaseManager, database_exists

def drop_all_tables():
    """删除所有表"""
    print("=== 开始删除表结构 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    print("警告: 你即将删除所有表结构！")
    print("此操作将永久删除所有表和数据，无法恢复！")
    
    confirm = input("请输入 'DROP' 确认删除: ")
    if confirm == 'DROP':
        # 自动检测表的外键依赖关系，按依赖顺序删除
        def get_table_dependencies(db):
            tables = []
            deps = {}
            # 获取所有表名
            table_rows = db.fetch_all("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            if table_rows:
                tables = [row[0] for row in table_rows]
            for table in tables:
                deps[table] = set()
                pragma = db.fetch_all(f"PRAGMA foreign_key_list({table})")
                if pragma:
                    for row in pragma:
                        deps[table].add(row[2])  # row[2] 是被依赖的表名
            return tables, deps
            
        def topo_sort(tables, deps):
            # 拓扑排序，返回可删除顺序
            visited = set()
            result = []
            def visit(table):
                if table in visited:
                    return
                visited.add(table)
                for dep in deps.get(table, []):
                    visit(dep)
                result.append(table)
            for t in tables:
                visit(t)
            # 逆序删除（先删无依赖的子表）
            return result[::-1]
            
        tables, deps = get_table_dependencies(db)
        delete_order = topo_sort(tables, deps)
        print(f"检测到的删除顺序: {delete_order}")
        success_count = 0
        for table in delete_order:
            if db.execute(f"DROP TABLE IF EXISTS {table}"):
                print(f"  表 {table} 删除成功")
                success_count += 1
            else:
                print(f"  表 {table} 删除失败")
        print(f"\n成功删除 {success_count} 个表\n")
    else:
        print("操作已取消！")

def drop_specific_table():
    """删除指定表"""
    print("=== 删除指定表 ===")
    
    if not database_exists():
        print("错误: 数据库不存在！")
        return False
    
    db = DatabaseManager()
    if not db.connect():
        return False
    
    # 获取所有表
    tables = db.fetch_all("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    
    if not tables:
        print("没有找到可删除的表")
        db.close()
        return True
    
    print("当前数据库中的表:")
    for i, table in enumerate(tables, 1):
        print(f"  {i}. {table[0]}")
    
    choice = input("\n请选择要删除的表编号(0取消): ")
    if choice == '0':
        print("取消删除操作")
        db.close()
        return True
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(tables):
            table_name = tables[index][0]
            
            print(f"\n警告: 你即将删除表 {table_name}！")
            confirm = input("请输入 'DROP' 确认删除: ")
            if confirm != 'DROP':
                print("取消删除操作")
                db.close()
                return True
            
            if db.execute(f"DROP TABLE IF EXISTS {table_name}"):
                print(f"表 {table_name} 删除成功！")
            else:
                print(f"表 {table_name} 删除失败！")
        else:
            print("无效的选择")
    
    except ValueError:
        print("请输入有效的数字")
    
    db.close()
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("          机票预订系统 - 表删除工具          ")
    print("=" * 50)
    print("⚠️  警告: 此工具将永久删除表结构和数据 ⚠️")
    print("=" * 50)
    
    while True:
        print("\n删除选项:")
        print("1. 删除所有表")
        print("2. 删除指定表")
        print("3. 退出")
        
        choice = input("\n请选择操作(1-3): ")
        
        if choice == '1':
            drop_all_tables()
        elif choice == '2':
            drop_specific_table()
        elif choice == '3':
            break
        else:
            print("无效的选择，请重新输入")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()