# Python 任务管理器（CLI + FastAPI）

这是一个使用 Python 编写的任务管理器，支持命令行操作和 HTTP API，用来练习 Python 基础、模块化开发和后端接口开发。两个入口共用业务逻辑和 JSON 存储。

## 已实现功能

- 新增任务
- 查看全部任务
- 通过 HTTP API 查询单个任务、按完成状态筛选、修改和删除任务
- 完成任务
- 设置任务优先级
- 使用 JSON 文件保存任务
- 使用 pytest 测试核心逻辑

## 技术要点

- Python 3.10+
- `dataclasses`：定义任务模型
- 模块拆分：模型、业务逻辑、数据存储、命令行入口
- `argparse`：解析命令行参数
- JSON：任务数据持久化
- pytest：自动化测试

## 项目结构

```text
python-task-cli/
├── api.py              # FastAPI 入口、请求校验和 HTTP 响应
├── main.py             # 命令行入口和结果展示
├── models.py           # Task 数据模型
├── service.py          # 新增、查找、完成、删除、筛选等业务逻辑
├── storage.py          # JSON 文件读写
├── tasks.json          # 运行时生成的任务数据
├── test/
│   ├── test_service.py # 业务逻辑测试
│   └── test_storage.py # JSON 存储测试
└── mai.py              # 早期菜单版程序，不是当前入口
```

命令行入口是 `main.py`，HTTP API 入口是 `api.py`。`mai.py` 是之前练习菜单式交互时留下的旧版本，可以保留作参考，也可以之后删除。

## 安装测试依赖

在项目根目录执行：

```powershell
python -m pip install pytest
```

## 使用方法

### 查看帮助

```powershell
python main.py --help
```

### 新增任务

```powershell
python main.py add "学习 Python"
python main.py add "学习 argparse" --priority high
```

优先级可以是：`low`、`medium` 或 `high`。

### 查看全部任务

```powershell
python main.py list
```

### 完成任务

```powershell
python main.py done 1
```

其中 `1` 是任务 ID，请根据 `list` 命令显示的实际 ID 替换。

## 运行测试

在项目根目录 `python-task-cli` 中，使用项目虚拟环境中的 Python 执行：

```powershell
python -m pytest -q
```

测试使用临时文件，不会覆盖项目中的真实 `tasks.json`。

## 模块职责

```text
main.py
负责解析命令行参数、显示结果，并协调其他模块

models.py
只定义 Task 数据结构

service.py
只处理任务业务逻辑，不负责用户输入、打印和文件保存

storage.py
负责从 tasks.json 读取任务，以及把任务保存回 JSON
```

## 项目运行示例

```text
> python main.py add "学习 Python" --priority high
任务添加成功：学习 Python

> python main.py list
1. 学习 Python [未完成] 优先级：high

> python main.py done 1
任务完成成功：学习 Python
```

## 当前限制

- 当前命令行版本支持 `add`、`list`、`done` 三个命令。
- 删除和未完成筛选逻辑已经在 `service.py` 中实现，但尚未接入 `main.py` 的命令行参数；搜索功能尚未实现。
- 数据保存在本地 `tasks.json`，暂未使用数据库。

## 学习收获

通过这个项目练习了：

- 函数和列表、字典的使用
- `dataclass` 和类型标注
- 模块化拆分
- 文件读写和 JSON 持久化
- 命令行参数解析
- 自动化测试和基本项目文档

## HTTP API 使用方法

### 创建环境和安装依赖

在项目根目录打开 PowerShell。首次使用时创建虚拟环境；已有 .venv 时跳过创建命令：

```powershell
python -m venv .venv
```

安装 API 和测试所需依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install fastapi "uvicorn[standard]" pytest
```

以下命令直接调用虚拟环境中的 Python，无须先激活环境。

### 启动服务

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --reload
```

api:app 表示 api.py 中的 app 对象。--reload 用于开发期间在代码保存后自动重新加载。保持此终端运行，按 Ctrl + C 停止服务；其他命令可以在新终端执行。

- [健康检查](http://127.0.0.1:8000/health)
- [任务列表](http://127.0.0.1:8000/tasks)
- [交互式接口文档](http://127.0.0.1:8000/docs)

根路径 / 暂未定义，直接访问 http://127.0.0.1:8000/ 会返回 404。

### 已实现接口

| 方法 | 路径 | 功能 | 成功状态码 |
| --- | --- | --- | --- |
| GET | /health | 检查服务能否响应，返回 {"status":"running"} | 200 |
| GET | /tasks | 返回全部任务，可通过 done 查询参数筛选；无匹配任务时返回 [] | 200 |
| POST | /tasks | 创建任务并保存到 JSON 文件 | 201 |
| GET | /tasks/{task_id} | 根据整数 ID 查询单个任务 | 200 |
| PATCH | /tasks/{task_id} | 部分修改任务并保存 | 200 |
| DELETE | /tasks/{task_id} | 删除任务并保存，返回确认信息和被删任务 | 200 |

健康检查中的 running 是自定义响应数据，与 HTTP 状态码是两个独立概念。

### 新增任务示例

在 /docs 中展开 POST /tasks，点击 Try it out，填写请求体后点击 Execute：

```json
{
  "title": "学习 FastAPI",
  "priority": "high"
}
```

title 必填；priority 可选，默认 medium，仅允许 low、medium、high。id 由服务端生成，done 默认为 false。

成功响应示例（实际 ID 取决于已有任务）：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "done": false,
  "priority": "high"
}
```

每次执行 POST 都会实际新增并保存一条任务。之后调用 GET /tasks 查看结果。

### 输入错误

- 标题为空字符串或全是空格：返回 400，响应为 {"detail":"任务标题不能为空"}。
- 缺少 title 或 priority 不在允许范围内：返回 422，由请求模型进行校验。

### 查询、筛选、修改与删除

- GET /tasks/1：查询 ID 为 1 的任务；请使用实际任务 ID。
- GET /tasks：返回全部任务。
- GET /tasks?done=true：只返回已完成任务。
- GET /tasks?done=false：只返回未完成任务。

省略 done 表示不筛选；false 是有效筛选条件。task_id 无法解析为整数、done 无法解析为布尔值时返回 422。

在 /docs 中调用 PATCH /tasks/{task_id}，可以只提交要修改的字段：

```json
{
  "done": false
}
```

也可以同时修改标题和优先级：

```json
{
  "title": "继续学习 FastAPI",
  "priority": "high"
}
```

未提供的字段保持原值。接口使用 model_dump(exclude_unset=True) 提取实际提交的字段，业务函数先校验再修改。

- 空请求体 {} 或已知字段显式传入 null：返回 400。
- 标题为空或全是空格：返回 400。
- 非法优先级：返回 422。
- 对不存在的任务进行查询、修改或删除：在请求参数和请求体合法时返回 404。

DELETE /tasks/{task_id} 成功后返回 200，响应示例：

```json
{
  "message": "任务已删除",
  "task": {
    "id": 1,
    "title": "删除接口测试",
    "done": false,
    "priority": "medium"
  }
}
```

再次查询或删除该 ID 会返回 404（前提是之后没有创建复用该 ID 的任务）。

### 第二天功能验收

1. 新增一条测试任务，记录 ID。
2. 按 ID 查询，验证不存在 ID 返回 404、非整数 ID 返回 422。
3. 分别筛选已完成和未完成任务，验证不传 done 时返回全部任务。
4. 单独修改标题、将 done 改为 true 再改为 false，确认未提交字段保持原值。
5. 验证空白标题、非法优先级、null 和空修改请求的错误响应。
6. 删除测试任务，确认其他任务保留，重复删除返回 404。
7. 重启服务，确认修改和删除结果已经保存。
8. 运行原有 pytest 测试。原有测试通过不代表新增修改逻辑和 HTTP 接口已获得完整自动化覆盖。

### 数据存储和模块协作

api.py 接收请求，使用 TaskCreate 校验创建参数，调用 service.py 处理业务，再调用 storage.py 读写文件，最后返回响应。

tasks.json 使用相对路径，因此 CLI 和 API 都应从项目根目录启动，才能使用同一个数据文件。重启服务后，任务会重新从文件读取。

当前存储实现遇到文件不存在时返回空列表；遇到无效 JSON 时打印提示并返回空列表。这不是完善的损坏恢复机制。当前文件存储也未处理并发写入，适用于本地学习，后续计划改用数据库。

### 验证方式

1. 调用 POST /tasks 新增任务，确认返回 201。
2. 调用 GET /tasks，确认能查询到新增任务。
3. 分别提交空白标题和非法优先级，确认返回 400 和 422。
4. 停止并重新启动服务，确认新增任务仍存在。
5. 在另一个终端执行已有测试：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

已有测试覆盖业务逻辑和存储；HTTP 接口目前采用手动验证，接口自动化测试待补充。以上步骤是验证方法，不代表每次修改后已自动执行。

### 后续计划

- 将 SQLite 数据库接入任务 API（目前已完成独立 SQL 练习）
- 接口自动化测试
- Docker 启动方式

## 第三天：SQLite 与 SQL 练习

db_practice.py 是独立学习脚本，使用 Python 内置 sqlite3，不需要安装数据库服务。现有 CLI 和 HTTP API 仍使用 tasks.json，尚未切换为数据库存储。

### 运行方式

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe db_practice.py
```

数据库 practice.db 位于脚本所在目录，首次连接时自动创建，已加入 .gitignore。新克隆项目运行脚本会得到空表，不会自动恢复本地练习数据。

脚本目前保留建表与查询，增删改和事务练习以注释形式保留。需要重做时只取消相应练习块的注释，包括配套的 commit；每次执行 INSERT 都会新增数据。CREATE TABLE IF NOT EXISTS 不会迁移已有表结构。

### 学习内容

- 表、行、列，以及整数主键。
- NOT NULL、DEFAULT 和 CHECK 约束；NOT NULL 本身不拒绝空字符串。
- INSERT 新增、SELECT 查询、UPDATE 修改、DELETE 删除。
- WHERE 筛选、ORDER BY 排序、LIMIT 限制结果数量。
- 使用 ? 占位符传参数，正确保存包含单引号的标题。
- fetchone() 返回一行或 None；fetchall() 返回结果列表。
- lastrowid 获取插入 ID，rowcount 查看受影响行数。
- commit() 提交，rollback() 撤销当前事务中未提交的修改。

### 事务练习

脚本中的两个 INSERT 之间不提交。使用当前连接方式时，第二条优先级为 urgent 会违反 CHECK 约束；捕获 IntegrityError 后显式 rollback，第一条插入也被撤销。

把第二条优先级设为 high，两条插入成功后统一 commit，任务数增加 2。提交后的修改不能通过后续 rollback 撤销。重新运行查询可以检查持久保存的结果。

UPDATE 和 DELETE 应检查 WHERE 条件，省略条件会影响整张表。仅注释 commit 并不会阻止 UPDATE 执行，同一连接中的查询仍可能看到尚未提交的修改。

### 验证记录与范围

练习通过终端手动验证，包括查询、修改、删除、失败回滚和成功提交。原有 10 个 pytest 测试已通过；这些原有测试不代表新增 SQLite 练习已被自动化测试覆盖。
