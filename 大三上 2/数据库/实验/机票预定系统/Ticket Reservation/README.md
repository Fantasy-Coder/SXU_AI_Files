# 机票预订系统完整解决方案

## 项目概述

本项目是一个基于Python SQLite的机票预订系统，完全覆盖数据库实验一的所有9个步骤。
✅ **实验步骤2: 修改数据库** - 已实现  
✅ **实验步骤3: 删除数据库** - 已实现  
✅ **实验步骤4: 创建表** - 已实现  
✅ **实验步骤5: 添加/查看/修改数据** - 已实现  
✅ **实验步骤6: 建立索引** - 已实现  
✅ **实验步骤7: 创建和使用视图** - 已实现  
✅ **实验步骤8: 各类查询和更新操作** - 已实现  
✅ **实验步骤9: 删除表、索引、视图** - 已实现  

## 项目结构

```

## 业务服务层与触发器

- 运行触发器配置（不改动现有表，仅新增审计表）：`python trigger_operations/trigger_demo_sqlite.py`
- 业务核心封装：`business_operations/service.py`（购票、支付、退票、改签、查询）。
- 演示流程：`python business_operations/demo_workflow.py`（搜索 -> 下单 -> 支付 -> 退票示例）。
- Streamlit 原型界面：
  1) `pip install streamlit prettytable`
  2) `streamlit run streamlit_app.py`

airline_ticket_system/
├── database_operations/     # 数据库操作模块
│   ├── create_database.py   # 1. 创建数据库
│   ├── modify_database.py   # 2. 修改数据库
│   └── drop_database.py     # 3. 删除数据库
├── table_operations/        # 表操作模块
│   ├── create_tables.py     # 4. 创建表
│   ├── insert_data.py       # 5. 插入数据
│   ├── query_data.py        # 5. 查询数据 & 8. 各类查询
│   └── drop_tables.py       # 9. 删除表
├── index_operations/        # 索引操作模块
│   ├── create_indexes.py    # 6. 建立索引
│   └── drop_indexes.py      # 9. 删除索引
├── cursor_operations/       # 游标操作模块（实验二扩展）
│   └── cursor_demo.py       # 游标功能演示
├── security_operations/     # 安全与权限（实验三示例，SQL Server）
│   └── security_demo.sql    # 登录/用户/角色/权限示例脚本
├── view_operations/         # 视图操作模块
│   ├── create_views.py      # 7. 创建视图
│   ├── query_views.py       # 7. 查询视图
│   └── drop_views.py        # 9. 删除视图
├── db_utils.py              # 数据库工具类
├── test_all_operations.py   # 综合测试工具
└── README.md                # 项目说明文档
```

## 环境要求

- Python 3.6+
- SQLite 3 (Python内置)
- 第三方库: prettytable

## 安装依赖

```bash
pip install prettytable
```

## 使用指南

### 快速开始 - 综合测试

```bash
python test_all_operations.py
```

这将引导您完成所有实验步骤的测试。

### 分步操作指南

#### 1. 数据库操作

```bash
# 创建数据库
python database_operations/create_database.py

# 修改数据库配置
python database_operations/modify_database.py

# 删除数据库
python database_operations/drop_database.py
```

#### 2. 表操作

```bash
# 创建表结构
python table_operations/create_tables.py

# 插入测试数据
python table_operations/insert_data.py

# 查询和修改数据
python table_operations/query_data.py

# 删除表
python table_operations/drop_tables.py
```

#### 3. 索引操作

```bash
# 创建索引
python index_operations/create_indexes.py

# 删除索引
python index_operations/drop_indexes.py
```

#### 4. 视图操作

```bash
# 创建视图
python view_operations/create_views.py

# 查询视图
python view_operations/query_views.py

# 删除视图
python view_operations/drop_views.py
```

#### 5. 游标功能（实验二扩展）

前置条件：已完成实验一（数据库、表、测试数据已创建）。如提示数据库不存在，请先运行 `python database_operations/create_database.py`；如表中无数据，请先运行 `python table_operations/insert_data.py`。

```bash
# 演示游标的声明、查询、更新、事务与关闭
python cursor_operations/cursor_demo.py
```

运行后选择 `1` 执行游标基本操作演示，按提示输入航班ID与新票价，观察事务提交/回滚与游标属性输出。

## 实验报告截图要点

在实验报告中需要截图的关键步骤：

1. **数据库创建成功界面** - `create_database.py` 执行结果
2. **表结构创建成功界面** - `create_tables.py` 执行结果  
3. **测试数据插入成功界面** - `insert_data.py` 执行结果
4. **数据查询结果界面** - `query_data.py` 执行结果
5. **索引创建成功界面** - `create_indexes.py` 执行结果
6. **视图创建成功界面** - `create_views.py` 执行结果
7. **视图查询结果界面** - `query_views.py` 执行结果
8. **游标操作关键界面** - `cursor_operations/cursor_demo.py` 执行结果，包括：
	- 成功获取游标对象
	- fetchone/fetchmany/fetchall 查询输出
	- 更新前后对比（输入航班ID与新票价后）
	- 事务提交成功（或回滚）提示
	- 游标属性展示（列名、列数等）
	- 游标关闭提示

#### 6. 安全与权限（实验三）

SQLite 版（应用层 RBAC 演示）
- 运行：`python security_operations/security_demo_sqlite.py`
- 前置：确保 `airline_ticket_system.db` 已存在且有 Flight / Orders / Customer 数据（实验一已生成）。
- 内置用户与角色：
	- `sysadmin_ticket` → admin（查询/增/改/删航班、订单；可查客户）
	- `ticket_agent` → agent（查询/增/改航班，查询/增订单，查询客户；禁止删航班）
	- `ticket_customer` → customer（查询航班，查看自身订单；禁止查客户表、禁止删/改航班）
- 演示操作：查询航班、更新票价、删除航班、查询客户、查看订单；按角色展示“允许/拒绝”。
- 截图要点：不同用户下的允许/拒绝输出对比。

SQL Server 版（如果有 SQL Server 环境）
- 脚本：`security_operations/security_demo.sql`
- 在 SQL Server 客户端执行（如 SSMS/sqlcmd），不可用 Python 运行。
- 账户：`sysadmin_ticket / Admin@123`，`ticket_agent / Agent@123`，`ticket_customer / Customer@123`
- 连接后执行：
	```sql
	USE TicketSystem;
	GO
	EXEC dbo.CheckUserPermissions;
	```
- 截图要点：角色识别、允许/拒绝操作、权限撤销/恢复前后对比。

## 技术特点

1. **模块化设计** - 每个功能模块独立，便于理解和维护
2. **用户友好界面** - 清晰的菜单和提示信息
3. **错误处理** - 完善的异常处理机制
4. **安全操作** - 重要操作需要确认，防止误操作
5. **性能优化** - 合理的索引设计提升查询性能

## 常见问题

### Q1: 运行脚本时提示"数据库不存在"

A: 请先运行 `create_database.py` 创建数据库，再运行其他脚本。

### Q2: 插入数据时提示"外键约束失败"

A: 确保表结构已正确创建，并且外键关联的表中存在相应的数据。

### Q3: 视图查询时没有数据

A: 确保已经插入了测试数据，并且视图依赖的表中存在数据。

## 扩展功能

## 实验七：存储过程（SQLite 模拟）

- SQLite 不支持原生存储过程，本项目在 `stored_procedure_operations/stored_procedure_demo_sqlite.py` 中用 Python 封装进行等价演示。
- 运行命令：`python stored_procedure_operations/stored_procedure_demo_sqlite.py`
- 覆盖操作：创建、执行、查看、修改 (ALTER)、重命名、删除存储过程（通过模拟器实现）。
- 示例场景：
	- 按学号查询课程成绩并计算平均分。
	- 按课程名查询选课学生及人数。
	- 修改学号并同步选课表。
	- 插入选课前验证学生/课程存在。

本项目可以进一步扩展以下功能：

1. **用户认证系统** - 实现用户登录和权限管理
2. **航班预订功能** - 实现完整的机票预订流程
3. **报表生成** - 生成各种统计报表
4. **数据备份与恢复** - 实现自动备份功能
5. **图形界面** - 使用Tkinter或PyQt创建GUI界面

## 总结

本解决方案完全覆盖了数据库实验一的所有要求，提供了一个完整的机票预订系统数据库实现。通过这个项目，您可以学习到：

- 数据库设计和实现的基本原理
- SQL语句的高级应用
- 索引和视图的优化使用
- Python数据库编程技术
- 软件工程的模块化设计思想

祝您实验顺利！