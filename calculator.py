import logging

def add(a, b):
    """加法函数 - 带日志记录"""
    logging.info(f"执行加法: {a} + {b}")
    return a + b

def subtract(a, b):
    """减法函数 - 带日志记录"""
    logging.info(f"main 修改减法函数: {a} + {b}")
    print(f"Subtracting {b} from {a}")
    return a - b

def multiply(a, b):
    """乘法函数 - 支持大数"""
     logging.info(f"main 修改乘法函数: {a} + {b}")
    return a * b

def divide(a, b):
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def power(a, b):
    """幂运算"""
    logging.info(f"执行幂运算: {a} + {b}")
    return a ** b
