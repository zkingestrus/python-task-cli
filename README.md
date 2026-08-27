# Python 命令行任务管理器

这是一个使用 Python 编写的命令行任务管理器，用来练习 Python 基础和小型项目的模块化开发。

## 已实现功能

- 新增任务
- 查看全部任务
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
learn/
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

当前正式入口是 `main.py`。`mai.py` 是之前练习菜单式交互时留下的旧版本，可以保留作参考，也可以之后删除。

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

必须在项目根目录 `learn` 中执行：

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
