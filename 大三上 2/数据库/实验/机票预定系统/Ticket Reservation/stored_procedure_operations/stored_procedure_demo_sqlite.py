"""
SQLite 版“存储过程”实验演示
- 通过 Python 封装模拟存储过程的创建、执行、查看、修改、重命名、删除
- 覆盖实验指导书实验七的核心步骤
- 使用 Student / Course / SC 三表与示例数据
"""
import os
import sqlite3
from typing import Callable, Dict, Any
from prettytable import PrettyTable

from db_utils import DatabaseManager


class StoredProcedureSimulator:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.procedures: Dict[str, Dict[str, Any]] = {}

    def create_proc(self, name: str, func: Callable, description: str, definition: str, params: str = ""):
        self.procedures[name] = {
            "func": func,
            "description": description,
            "definition": definition,
            "params": params,
        }
        print(f"[CREATE] 存储过程 {name} 已注册")

    def execute_proc(self, name: str, **kwargs):
        if name not in self.procedures:
            print(f"[EXEC] 存储过程 {name} 不存在")
            return
        print(f"\n[EXEC] 执行 {name} {kwargs}")
        self.procedures[name]["func"](**kwargs)

    def show_proc(self, name: str):
        proc = self.procedures.get(name)
        if not proc:
            print(f"[SHOW] 存储过程 {name} 不存在")
            return
        print(f"\n[SHOW] {name}")
        print(f"描述: {proc['description']}")
        if proc.get("params"):
            print(f"参数: {proc['params']}")
        print("定义/伪代码:\n" + proc["definition"])

    def alter_proc(self, name: str, new_func: Callable, new_description: str, new_definition: str, new_params: str = ""):
        if name not in self.procedures:
            print(f"[ALTER] 存储过程 {name} 不存在")
            return
        self.procedures[name].update({
            "func": new_func,
            "description": new_description,
            "definition": new_definition,
            "params": new_params,
        })
        print(f"[ALTER] 存储过程 {name} 已更新")

    def rename_proc(self, old_name: str, new_name: str):
        if old_name not in self.procedures:
            print(f"[RENAME] 存储过程 {old_name} 不存在")
            return
        if new_name in self.procedures:
            print(f"[RENAME] 目标名称 {new_name} 已存在")
            return
        self.procedures[new_name] = self.procedures.pop(old_name)
        print(f"[RENAME] {old_name} -> {new_name} 完成")

    def drop_proc(self, name: str):
        if name not in self.procedures:
            print(f"[DROP] 存储过程 {name} 不存在")
            return
        self.procedures.pop(name)
        print(f"[DROP] 存储过程 {name} 已删除")

    def list_procs(self):
        print("\n[LIST] 当前已注册的存储过程")
        table = PrettyTable(["名称", "描述", "参数"])
        for name, meta in self.procedures.items():
            table.add_row([name, meta["description"], meta.get("params", "")])
        print(table)


def ensure_schema(db: DatabaseManager):
    sql_script = """
    CREATE TABLE IF NOT EXISTS Student(
        StudentNo TEXT PRIMARY KEY,
        StudentName TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Course(
        CourseNo TEXT PRIMARY KEY,
        CourseName TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS SC(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentNo TEXT NOT NULL,
        CourseNo TEXT NOT NULL,
        Grade INTEGER,
        FOREIGN KEY(StudentNo) REFERENCES Student(StudentNo) ON DELETE CASCADE,
        FOREIGN KEY(CourseNo) REFERENCES Course(CourseNo) ON DELETE CASCADE
    );
    """
    db.execute_script(sql_script)


def seed_data(db: DatabaseManager):
    if db.fetch_one("SELECT COUNT(1) FROM Student")[0] == 0:
        students = [
            ("2023001", "Alice"),
            ("2023002", "Bob"),
            ("2023003", "Carol"),
        ]
        db.cursor.executemany("INSERT INTO Student(StudentNo, StudentName) VALUES(?, ?)", students)
        db.conn.commit()

    if db.fetch_one("SELECT COUNT(1) FROM Course")[0] == 0:
        courses = [
            ("C01", "Database"),
            ("C02", "Algorithms"),
            ("C03", "Operating Systems"),
        ]
        db.cursor.executemany("INSERT INTO Course(CourseNo, CourseName) VALUES(?, ?)", courses)
        db.conn.commit()

    if db.fetch_one("SELECT COUNT(1) FROM SC")[0] == 0:
        sc_rows = [
            ("2023001", "C01", 95),
            ("2023001", "C02", 88),
            ("2023002", "C01", 76),
            ("2023002", "C03", 90),
            ("2023003", "C02", 82),
        ]
        db.cursor.executemany("INSERT INTO SC(StudentNo, CourseNo, Grade) VALUES(?, ?, ?)", sc_rows)
        db.conn.commit()


# --- 伪存储过程函数定义 ---

def proc_get_student_scores(db: DatabaseManager, student_no: str):
    rows = db.fetch_all(
        """
        SELECT s.StudentNo, s.StudentName, c.CourseName, sc.Grade
        FROM SC sc
        JOIN Student s ON sc.StudentNo = s.StudentNo
        JOIN Course c ON sc.CourseNo = c.CourseNo
        WHERE s.StudentNo = ?
        ORDER BY c.CourseName
        """,
        (student_no,),
    )
    avg_grade = db.fetch_one("SELECT ROUND(AVG(Grade),2) FROM SC WHERE StudentNo=?", (student_no,))[0]
    table = PrettyTable(["学号", "姓名", "课程", "成绩"])
    for r in rows:
        table.add_row(r)
    print(table)
    print(f"平均成绩: {avg_grade if avg_grade is not None else '无记录'}")


def proc_get_course_students(db: DatabaseManager, course_name: str):
    rows = db.fetch_all(
        """
        SELECT c.CourseNo, c.CourseName, s.StudentName, sc.Grade
        FROM SC sc
        JOIN Course c ON sc.CourseNo = c.CourseNo
        JOIN Student s ON sc.StudentNo = s.StudentNo
        WHERE c.CourseName = ?
        ORDER BY sc.Grade DESC
        """,
        (course_name,),
    )
    table = PrettyTable(["课程号", "课程名", "学生", "成绩"])
    for r in rows:
        table.add_row(r)
    print(table)
    print(f"选课学生总数: {len(rows)}")


def proc_update_student_id(db: DatabaseManager, old_id: str, new_id: str):
    exists_new = db.fetch_one("SELECT 1 FROM Student WHERE StudentNo=?", (new_id,))
    if exists_new:
        print(f"新学号 {new_id} 已存在，无法修改")
        return
    updated = db.execute("UPDATE Student SET StudentNo=? WHERE StudentNo=?", (new_id, old_id))
    if updated:
        db.execute("UPDATE SC SET StudentNo=? WHERE StudentNo=?", (new_id, old_id))
        print(f"已将学号 {old_id} -> {new_id}，并同步选课表")


def proc_validate_student_before_enroll(db: DatabaseManager, student_no: str, course_no: str, grade: int = None):
    exists_student = db.fetch_one("SELECT 1 FROM Student WHERE StudentNo=?", (student_no,))
    if not exists_student:
        print(f"学生 {student_no} 不存在，禁止插入选课记录")
        return
    exists_course = db.fetch_one("SELECT 1 FROM Course WHERE CourseNo=?", (course_no,))
    if not exists_course:
        print(f"课程 {course_no} 不存在，禁止插入选课记录")
        return
    db.execute("INSERT INTO SC(StudentNo, CourseNo, Grade) VALUES(?, ?, ?)", (student_no, course_no, grade))
    print(f"已为学生 {student_no} 选课 {course_no} (成绩 {grade})")


def proc_get_student_scores_v2(db: DatabaseManager, student_no: str):
    rows = db.fetch_all(
        """
        SELECT s.StudentNo, s.StudentName, c.CourseName, sc.Grade
        FROM SC sc
        JOIN Student s ON sc.StudentNo = s.StudentNo
        JOIN Course c ON sc.CourseNo = c.CourseNo
        WHERE s.StudentNo = ?
        ORDER BY sc.Grade DESC
        """,
        (student_no,),
    )
    agg = db.fetch_one(
        "SELECT ROUND(AVG(Grade),2), MAX(Grade), MIN(Grade) FROM SC WHERE StudentNo=?",
        (student_no,),
    )
    table = PrettyTable(["学号", "姓名", "课程", "成绩"])
    for r in rows:
        table.add_row(r)
    print(table)
    if agg:
        avg_g, max_g, min_g = agg
        print(f"平均: {avg_g}  最高: {max_g}  最低: {min_g}")


# --- 演示流程 ---

def run_demo():
    db = DatabaseManager()
    if not db.connect():
        return
    ensure_schema(db)
    seed_data(db)

    simulator = StoredProcedureSimulator(db)

    simulator.create_proc(
        name="proc_get_student_scores",
        func=lambda student_no: proc_get_student_scores(db, student_no),
        description="根据学号查询课程成绩并给出平均分",
        definition="""
        -- 输入: @student_no
        SELECT CourseName, Grade FROM SC JOIN Course USING(CourseNo)
        WHERE StudentNo=@student_no;
        SELECT AVG(Grade) ...;
        """,
        params="@student_no TEXT",
    )

    simulator.create_proc(
        name="proc_get_course_students",
        func=lambda course_name: proc_get_course_students(db, course_name),
        description="按课程名列出选课学生及人数",
        definition="""
        -- 输入: @course_name
        SELECT StudentName, Grade FROM SC JOIN Student USING(StudentNo)
        JOIN Course USING(CourseNo) WHERE CourseName=@course_name;
        """,
        params="@course_name TEXT",
    )

    simulator.create_proc(
        name="proc_update_student_id",
        func=lambda old_id, new_id: proc_update_student_id(db, old_id, new_id),
        description="修改学号并同步选课表",
        definition="""
        -- 输入: @old_id, @new_id
        UPDATE Student SET StudentNo=@new_id WHERE StudentNo=@old_id;
        UPDATE SC SET StudentNo=@new_id WHERE StudentNo=@old_id;
        """,
        params="@old_id TEXT, @new_id TEXT",
    )

    simulator.create_proc(
        name="proc_validate_student_before_enroll",
        func=lambda student_no, course_no, grade=None: proc_validate_student_before_enroll(db, student_no, course_no, grade),
        description="插入选课前验证学生/课程存在",
        definition="""
        -- 输入: @student_no, @course_no, @grade
        IF NOT EXISTS(Student) RAISERROR ...
        IF NOT EXISTS(Course) RAISERROR ...
        INSERT INTO SC(StudentNo, CourseNo, Grade) VALUES(...);
        """,
        params="@student_no TEXT, @course_no TEXT, @grade INT",
    )

    simulator.list_procs()

    simulator.execute_proc("proc_get_student_scores", student_no="2023001")
    simulator.execute_proc("proc_get_course_students", course_name="Database")
    simulator.execute_proc("proc_update_student_id", old_id="2023003", new_id="2023999")
    simulator.execute_proc("proc_validate_student_before_enroll", student_no="2023999", course_no="C03", grade=91)

    simulator.show_proc("proc_get_student_scores")

    simulator.alter_proc(
        name="proc_get_student_scores",
        new_func=lambda student_no: proc_get_student_scores_v2(db, student_no),
        new_description="查询成绩，输出平均/最高/最低",
        new_definition="""
        -- 输入: @student_no
        SELECT CourseName, Grade FROM ... ORDER BY Grade DESC;
        SELECT AVG(Grade), MAX(Grade), MIN(Grade) FROM SC WHERE StudentNo=@student_no;
        """,
        new_params="@student_no TEXT",
    )

    simulator.execute_proc("proc_get_student_scores", student_no="2023001")

    simulator.rename_proc("proc_get_course_students", "proc_get_course_students_v2")
    simulator.drop_proc("proc_validate_student_before_enroll")

    simulator.list_procs()
    db.close()


if __name__ == "__main__":
    run_demo()
