from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("practice.db")

conn = sqlite3.connect(DB_PATH)

try:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
            priority TEXT NOT NULL DEFAULT 'medium'
                CHECK (priority IN ('low', 'medium', 'high'))
        )
    """)



    # cursor = conn.execute(
    #     "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
    #     ("完成 SQLite 查询练习", 1, 1),
    # )

    # conn.commit()
    # print(f"修改了 {cursor.rowcount} 条任务")





    # cursor = conn.execute(
    #     "INSERT INTO tasks (title, priority) VALUES (?, ?)",
    #     ("学习 SQLite", "high"),
    # )

    # conn.commit()

    # print(f"新增任务成功，ID：{cursor.lastrowid}")





    cursor = conn.execute(
        "SELECT id, title, done, priority FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)





    print("查询 ID 为 1 的任务：")

    cursor = conn.execute(
        "SELECT id, title, done, priority FROM tasks WHERE id = ?",
        (1,),
    )

    task = cursor.fetchone()
    print(task)

    print("查询所有未完成任务：")

    cursor = conn.execute(
        "SELECT id, title, done, priority FROM tasks "
        "WHERE done = ? ORDER BY id",
        (0,),
    )

    tasks = cursor.fetchall()
    print(tasks)




    # # 新增一条专门用于删除的任务
    # cursor = conn.execute(
    #     "INSERT INTO tasks (title) VALUES (?)",
    #     ("删除练习任务",),
    # )
    # test_id = cursor.lastrowid
    # conn.commit()

    # # 按 ID 删除它
    # cursor = conn.execute(
    #     "DELETE FROM tasks WHERE id = ?",
    #     (test_id,),
    # )
    # conn.commit()
    # print(f"删除了 {cursor.rowcount} 条任务")

    # # 验证已删除
    # cursor = conn.execute(
    #     "SELECT id, title FROM tasks WHERE id = ?",
    #     (test_id,),
    # )
    # print("删除后查询：", cursor.fetchone())

    # # 确认其他任务仍然存在
    # cursor = conn.execute(
    #     "SELECT id, title, done, priority FROM tasks ORDER BY id"
    # )
    # print("剩余任务：", cursor.fetchall())




    # before = conn.execute(
    #     "SELECT COUNT(*) FROM tasks"
    # ).fetchone()[0]

    # try:
    #     conn.execute(
    #         "INSERT INTO tasks (title, priority) VALUES (?, ?)",
    #         ("事务练习：第一条", "medium"),
    #     )

    #     # 使用 high 验证提交；改为 urgent 可触发 CHECK 约束并验证回滚
    #     conn.execute(
    #         "INSERT INTO tasks (title, priority) VALUES (?, ?)",
    #         ("事务练习：第二条", "high"),
    #     )

    #     conn.commit()
    #     print("事务提交成功")

    # except sqlite3.IntegrityError as exc:
    #     conn.rollback()
    #     print("数据违反约束，已回滚：", exc)

    # after = conn.execute(
    #     "SELECT COUNT(*) FROM tasks"
    # ).fetchone()[0]

    # print("操作前任务数：", before)
    # print("操作后任务数：", after)

 

    # rows = conn.execute(
    #     "SELECT id, title FROM tasks ORDER BY id DESC LIMIT ?",
    #     (2,),
    # ).fetchall()

    # print("ID 最大的两条任务：", rows)

    # cursor = conn.execute(
    #     "INSERT INTO tasks (title) VALUES (?)",
    #     ("阅读 Python's sqlite3 文档",),
    # )
    # new_id = cursor.lastrowid
    # conn.commit()

    # row = conn.execute(
    #     "SELECT id, title FROM tasks WHERE id = ?",
    #     (new_id,),
    # ).fetchone()

    # print("包含单引号的任务：", row)

    
finally:
    conn.close()