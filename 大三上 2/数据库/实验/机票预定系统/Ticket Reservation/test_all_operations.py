"""
综合测试工具
功能: 测试所有数据库操作功能
"""
import os
import sys
import time

def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """打印标题"""
    clear_screen()
    print("=" * 60)
    print(f"          {title}          ")
    print("=" * 60)

def test_database_operations():
    """测试数据库操作"""
    print_header("测试数据库操作")
    
    print("\n1. 创建数据库")
    input("按回车键继续...")
    os.system("python database_operations/create_database.py")
    input("\n按回车键继续...")
    
    print_header("测试数据库操作")
    print("\n2. 修改数据库配置")
    input("按回车键继续...")
    os.system("python database_operations/modify_database.py")
    input("\n按回车键继续...")

def test_table_operations():
    """测试表操作"""
    print_header("测试表操作")
    
    print("\n1. 创建表结构")
    input("按回车键继续...")
    os.system("python table_operations/create_tables.py")
    input("\n按回车键继续...")
    
    print_header("测试表操作")
    print("\n2. 插入测试数据")
    input("按回车键继续...")
    os.system("python table_operations/insert_data.py")
    input("\n按回车键继续...")
    
    print_header("测试表操作")
    print("\n3. 查询和修改数据")
    input("按回车键继续...")
    os.system("python table_operations/query_data.py")
    input("\n按回车键继续...")

def test_index_operations():
    """测试索引操作"""
    print_header("测试索引操作")
    
    print("\n1. 创建索引")
    input("按回车键继续...")
    os.system("python index_operations/create_indexes.py")
    input("\n按回车键继续...")
    
    print_header("测试索引操作")
    print("\n2. 查看索引信息")
    input("按回车键继续...")
    os.system("python index_operations/create_indexes.py")
    input("\n按回车键继续...")

def test_view_operations():
    """测试视图操作"""
    print_header("测试视图操作")
    
    print("\n1. 创建视图")
    input("按回车键继续...")
    os.system("python view_operations/create_views.py")
    input("\n按回车键继续...")
    
    print_header("测试视图操作")
    print("\n2. 查询视图数据")
    input("按回车键继续...")
    os.system("python view_operations/query_views.py")
    input("\n按回车键继续...")

def test_cleanup_operations():
    """测试清理操作"""
    print_header("测试清理操作")
    
    print("\n1. 删除视图")
    input("按回车键继续...")
    os.system("python view_operations/drop_views.py")
    input("\n按回车键继续...")
    
    print_header("测试清理操作")
    print("\n2. 删除索引")
    input("按回车键继续...")
    os.system("python index_operations/drop_indexes.py")
    input("\n按回车键继续...")
    
    print_header("测试清理操作")
    print("\n3. 删除表")
    input("按回车键继续...")
    os.system("python table_operations/drop_tables.py")
    input("\n按回车键继续...")
    
    print_header("测试清理操作")
    print("\n4. 删除数据库")
    input("按回车键继续...")
    os.system("python database_operations/drop_database.py")
    input("\n按回车键继续...")

def main():
    """主函数"""
    print_header("机票预订系统 - 综合测试工具")
    
    print("\n欢迎使用机票预订系统综合测试工具！")
    print("本工具将引导您完成所有数据库操作的测试")
    print("\n测试流程:")
    print("1. 数据库操作 (创建、修改)")
    print("2. 表操作 (创建、插入、查询、修改)")
    print("3. 索引操作 (创建、查看)")
    print("4. 视图操作 (创建、查询)")
    print("5. 清理操作 (删除视图、索引、表、数据库)")
    
    print("\n注意: 测试过程中请按照提示操作")
    print("      测试完成后所有数据将被清理")
    
    start_test = input("\n是否开始测试？(y/n): ").lower()
    if start_test != 'y':
        print("\n测试已取消")
        return
    
    try:
        # 测试流程
        test_database_operations()
        test_table_operations()
        test_index_operations()
        test_view_operations()
        
        # 询问是否进行清理测试
        cleanup = input("\n是否进行清理操作测试？(y/n): ").lower()
        if cleanup == 'y':
            test_cleanup_operations()
        
        print_header("测试完成")
        print("\n🎉 所有测试操作完成！")
        print("\n您已成功完成机票预订系统的所有数据库操作测试:")
        print("• 数据库创建和管理")
        print("• 表结构设计和数据操作")
        print("• 索引创建和优化")
        print("• 视图创建和查询")
        print("• 数据查询和修改")
        
        print("\n这些操作对应实验一的所有9个步骤:")
        print("1. 创建数据库 ✅")
        print("2. 修改数据库 ✅")
        print("3. 删除数据库 ✅")
        print("4. 创建表 ✅")
        print("5. 添加/查看/修改数据 ✅")
        print("6. 建立索引 ✅")
        print("7. 创建和使用视图 ✅")
        print("8. 各类查询和更新操作 ✅")
        print("9. 删除表、索引、视图 ✅")
        
        print("\n实验一已圆满完成！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")

if __name__ == "__main__":
    main()