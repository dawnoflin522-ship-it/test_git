def add(a, b):
    """数"""
    return float(a) + float(b)

def subtract(a, b):
    """减法函数 - 带日志记录"""
    print(f"Subtracting {b} from {a}")
    return a - b

def multiply(a, b):
    """乘法函数 - 支持大数"""
    return a * b

def divide(a, b):
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def power(a, b):
    """幂运算"""
    return a ** b
