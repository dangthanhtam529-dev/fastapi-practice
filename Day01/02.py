# =============================================================================
# FastAPI 类型提示系统 - 数值类型与联合类型示例
# =============================================================================
# 本文件演示了以下重要的类型提示概念：
# 1. 整数类型到字符串的自动转换
# 2. 联合类型（Union Types）：一个变量可以是多种类型之一
# 3. 可空类型（Optional）：变量可以是某种类型或 None
#
# 【类型转换问题】
# 在 Python 中，字符串和整数不能直接拼接：
#   "John is " + 25  # TypeError: can only concatenate str (not "int") to str
#
# 必须先将整数转换为字符串：
#   "John is " + str(25)  # "John is 25"
#
# 【联合类型（Union Types）】
# 使用 "|" 操作符可以表示一个变量可以是多种类型之一：
#   age: int | float  # age 可以是整数或浮点数
#
# 【可空类型（Optional）】
# 使用 "X | None" 或 "Optional[X]" 表示变量可以是该类型或 None：
#   age: int | None  # age 可以是整数，也可以是 None
#
# 【示例 1：基础类型转换】
# 定义一个函数，接受姓名（字符串）和年龄（整数）
# 在拼接字符串时，必须使用 str() 将整数转换为字符串
# 如果不这样做，代码会报错：TypeError
def get_name_with_age(name: str, age: int) -> str:
    """
    获取包含年龄的姓名描述

    Args:
        name: 姓名，字符串类型
        age: 年龄，整数类型

    Returns:
        格式化的字符串，描述姓名和年龄
    """
    # 注意：这里必须使用 str(age) 将整数转换为字符串
    # 如果直接写 name + " is this old: " + age 会报错
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


# 【示例 2：联合类型】
# 定义一个函数，age 参数可以是整数或浮点数
# 这样函数更加灵活，可以处理年龄为小数的情况（如 25.5）
def get_name_with_age(name: str, age: int | float) -> str:
    """
    获取包含年龄的姓名描述（支持浮点年龄）

    Args:
        name: 姓名，字符串类型
        age: 年龄，可以是整数或浮点数

    Returns:
        格式化的字符串，描述姓名和年龄
    """
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


# 【示例 3：可空类型】
# 定义一个函数，age 参数可以是整数、浮点数或 None
# 如果 age 为 None，表示该人没有年龄信息
# 使用默认参数 None，可以使参数变成可选的
def get_name_with_age(name: str, age: int | float | None = None) -> str:
    """
    获取包含年龄的姓名描述（支持空值）

    Args:
        name: 姓名，字符串类型
        age: 年龄，可以是整数、浮点数或 None（可选参数）

    Returns:
        格式化的字符串，描述姓名和年龄
    """
    # 检查 age 是否为 None
    if age is None:
        # 如果没有年龄信息，返回特殊格式的字符串
        name_with_age = name + " has no age"
    else:
        # 如果有年龄信息，格式化输出
        name_with_age = name + " is this old: " + str(age)
    return name_with_age


# 测试示例
if __name__ == '__main__':
    # 测试示例 1
    print(get_name_with_age("John", 25))  # John is this old: 25

    # 测试示例 2（浮点数年龄）
    print(get_name_with_age("Jane", 25.5))  # Jane is this old: 25.5

    # 测试示例 3（可空类型）
    print(get_name_with_age("Unknown", None))  # Unknown has no age
    print(get_name_with_age("Alice"))  # Alice has no age（使用默认值 None）
