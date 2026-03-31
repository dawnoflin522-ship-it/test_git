# Git 冲突演示指南

本指南演示 Git 中两种常见的冲突类型：Merge 冲突 和 Rebase 冲突。

---

## 场景一：Merge 冲突演示

### 冲突产生的原因
当两个分支同时修改了同一个文件的同一部分，Git 无法自动决定使用哪个版本时，就会产生 merge 冲突。

### 演示步骤

#### 1. 初始化仓库
```bash
git init
git config user.name "Demo User"
git config user.email "demo@example.com"
```

#### 2. 创建基础文件并提交
创建 [calculator.py](calculator.py):
```python
def add(a, b):
    """加法函数"""
    return a + b

def subtract(a, b):
    """减法函数"""
    return a - b
```

```bash
git add calculator.py
git commit -m "Initial commit: basic calculator"
```

#### 3. 创建 feature 分支并修改
```bash
git checkout -b feature-add-logging
```

修改 `add` 函数，添加日志：
```python
import logging

def add(a, b):
    """加法函数 - 带日志记录"""
    logging.info(f"执行加法: {a} + {b}")
    return a + b
```

```bash
git add calculator.py
git commit -m "Feature: add logging to add function"
```

#### 4. 回到 master 分支，修改同一行
```bash
git checkout master
```

修改 `add` 函数，支持浮点数：
```python
def add(a, b):
    """加法函数 - 支持浮点数"""
    return float(a) + float(b)
```

```bash
git add calculator.py
git commit -m "Master: improve add function to support float"
```

#### 5. 执行 Merge，产生冲突
```bash
git merge feature-add-logging
```

**输出：**
```
Auto-merging calculator.py
CONFLICT (content): Merge conflict in calculator.py
Automatic merge failed; fix conflicts and then commit the result.
```

#### 6. 查看冲突文件
打开 [calculator.py](calculator.py)，会看到冲突标记：
```python
<<<<<<< HEAD
    """加法函数 - 支持浮点数"""
    return float(a) + float(b)
=======
    """加法函数 - 带日志记录"""
    logging.info(f"执行加法: {a} + {b}")
    return a + b
>>>>>>> feature-add-logging
```

**冲突标记说明：**
- `<<<<<<< HEAD`：当前分支（master）的内容
- `=======`：分隔线
- `>>>>>>> feature-add-logging`：要合并的分支内容

#### 7. 解决冲突
编辑文件，合并两个版本的改动：
```python
import logging

def add(a, b):
    """加法函数 - 支持浮点数并带日志记录"""
    logging.info(f"执行加法: {a} + {b}")
    return float(a) + float(b)
```

#### 8. 完成合并
```bash
git add calculator.py
git commit -m "Resolved merge conflict: combined float support and logging"
```

---

## 场景二：Rebase 冲突演示

### 冲突产生的原因
Rebase 冲突与 merge 冲突类似，但发生在 rebase 过程中。当 rebase 尝试将一个分支的提交应用到另一个分支时，如果修改了相同的位置，就会产生冲突。

### 演示步骤

#### 1. 从 master 创建 feature 分支
```bash
git checkout -b feature-rebase-demo
```

#### 2. 添加新文件并提交
创建 [utils.py](utils.py):
```python
def format_number(n):
    """格式化数字"""
    return str(n)
```

```bash
git add utils.py
git commit -m "Add utils module"
```

#### 3. 修改 calculator.py 的 subtract 函数
```python
def subtract(a, b):
    """减法函数 - 带日志记录"""
    print(f"Subtracting {b} from {a}")
    return a - b
```

```bash
git add calculator.py
git commit -m "Add logging to subtract function"
```

#### 4. 回到 master，修改同一个函数
```bash
git checkout master
```

修改 `subtract` 函数：
```python
def subtract(a, b):
    """减法函数 - 支持负数结果"""
    result = a - b
    return result
```

```bash
git add calculator.py
git commit -m "Improve subtract to support negative results"
```

#### 5. 执行 Rebase，产生冲突
```bash
git checkout feature-rebase-demo
git rebase master
```

**输出：**
```
Auto-merging calculator.py
CONFLICT (content): Merge conflict in calculator.py
Resolve all conflicts manually, mark them as resolved with
"git add/rm <conflicted_files>", then run "git rebase --continue".
```

#### 6. 查看冲突文件
冲突标记与 merge 类似：
```python
<<<<<<< HEAD
    """减法函数 - 支持负数结果"""
    result = a - b
    return result
=======
    """减法函数 - 带日志记录"""
    print(f"Subtracting {b} from {a}")
    return a - b
>>>>>>> Add logging to subtract function
```

#### 7. 解决冲突
编辑文件，合并改动：
```python
def subtract(a, b):
    """减法函数 - 支持负数结果并带日志"""
    print(f"Subtracting {b} from {a}")
    result = a - b
    return result
```

#### 8. 继续 Rebase
```bash
git add calculator.py
git rebase --continue
```

---

## Merge vs Rebase 冲突的区别

| 特性 | Merge 冲突 | Rebase 冲突 |
|------|-----------|-------------|
| 产生时机 | 合并两个分支时 | 变基（重放提交）时 |
| 解决后操作 | `git commit` | `git rebase --continue` |
| 历史记录 | 保留分支历史，有合并提交 | 线性历史，无合并提交 |
| 冲突解决次数 | 一次性解决所有冲突 | 可能多次解决（每个提交都可能冲突） |
| 中止命令 | `git merge --abort` | `git rebase --abort` |

---

## 常用命令总结

### 查看冲突状态
```bash
git status
```

### 查看冲突详情
```bash
git diff
```

### 中止合并/变基
```bash
git merge --abort    # 中止 merge
git rebase --abort   # 中止 rebase
```

### 标记冲突已解决
```bash
git add <file>
```

### 完成操作
```bash
git commit           # merge 完成后
git rebase --continue # rebase 完成后
```

---

## 冲突解决最佳实践

1. **理解冲突原因**：先理解两个分支分别做了什么改动
2. **与团队沟通**：如果不确定哪个版本正确，与相关开发者确认
3. **测试代码**：解决冲突后，务必测试代码是否正常工作
4. **保持原子性**：一个提交只解决一个冲突，不要混入其他改动
5. **使用工具**：可以使用 IDE 或专门的合并工具（如 Beyond Compare、KDiff3）

---

## 演示文件说明

- [calculator.py](calculator.py) - 演示用的计算器代码
- [utils.py](utils.py) - 工具函数模块
- [setup_demo.ps1](setup_demo.ps1) - 自动化设置脚本（可选）

现在你可以按照上述步骤手动操作，体验 Git 冲突的产生和解决过程！
