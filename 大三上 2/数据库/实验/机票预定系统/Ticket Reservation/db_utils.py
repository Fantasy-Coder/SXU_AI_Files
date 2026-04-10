import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='airline_ticket_system.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """连接数据库"""
        try:
            # 允许跨线程使用同一连接以兼容 Streamlit 多线程回调
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            # 启用外键约束
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except Exception as e:
            print(f"数据库连接错误: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def execute(self, sql, params=None):
        """执行SQL语句"""
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"执行SQL错误: {e}")
            print(f"SQL语句: {sql}")
            if params:
                print(f"参数: {params}")
            self.conn.rollback()
            return False
    
    def execute_script(self, sql_script):
        """执行SQL脚本"""
        try:
            self.cursor.executescript(sql_script)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"执行SQL脚本错误: {e}")
            self.conn.rollback()
            return False
    
    def fetch_all(self, sql, params=None):
        """查询所有结果"""
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"查询错误: {e}")
            return None
    
    def fetch_one(self, sql, params=None):
        """查询单条结果"""
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"查询错误: {e}")
            return None
    
    def get_last_insert_id(self):
        """获取最后插入的ID"""
        return self.cursor.lastrowid
    
    def get_table_schema(self, table_name):
        """获取表结构"""
        sql = "PRAGMA table_info(?)"
        return self.fetch_all(sql, (table_name,))
    
    def get_database_info(self):
        """获取数据库信息"""
        # 获取所有表
        tables = self.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
        # 获取所有索引
        indexes = self.fetch_all("SELECT name FROM sqlite_master WHERE type='index'")
        # 获取所有视图
        views = self.fetch_all("SELECT name FROM sqlite_master WHERE type='view'")
        
        return {
            'tables': [table[0] for table in tables] if tables else [],
            'indexes': [index[0] for index in indexes] if indexes else [],
            'views': [view[0] for view in views] if views else []
        }

# 数据库操作工具函数
def database_exists(db_name='airline_ticket_system.db'):
    """检查数据库是否存在"""
    return os.path.exists(db_name)

def backup_database(db_name='airline_ticket_system.db', backup_name=None):
    """备份数据库"""
    if not backup_name:
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{db_name}"
    
    try:
        # 创建新的数据库连接用于备份
        conn = sqlite3.connect(db_name)
        backup_conn = sqlite3.connect(backup_name)
        
        # 执行备份
        conn.backup(backup_conn)
        
        conn.close()
        backup_conn.close()
        
        print(f"数据库备份成功: {backup_name}")
        return True
    except Exception as e:
        print(f"数据库备份失败: {e}")
        return False

def restore_database(backup_name, db_name='airline_ticket_system.db'):
    """恢复数据库"""
    try:
        # 先关闭可能存在的连接
        if os.path.exists(db_name):
            os.remove(db_name)
        
        # 创建新的数据库连接用于恢复
        conn = sqlite3.connect(db_name)
        backup_conn = sqlite3.connect(backup_name)
        
        # 执行恢复
        backup_conn.backup(conn)
        
        conn.close()
        backup_conn.close()
        
        print(f"数据库恢复成功: {db_name}")
        return True
    except Exception as e:
        print(f"数据库恢复失败: {e}")
        return False

if __name__ == "__main__":
    # 测试数据库工具类
    db = DatabaseManager()
    if db.connect():
        print("数据库连接成功！")
        
        # 测试获取数据库信息
        db_info = db.get_database_info()
        print("\n数据库信息:")
        print(f"表: {db_info['tables']}")
        print(f"索引: {db_info['indexes']}")
        print(f"视图: {db_info['views']}")
        
        db.close()
    else:
        print("数据库连接失败！")