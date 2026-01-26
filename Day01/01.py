# =============================================================================
# FastAPI 类型提示系统 - 字符串类型提示示例
# =============================================================================
# 本文件演示了 Python 类型提示（Type Hints）在 FastAPI 中的重要作用
#
# 【为什么要使用类型提示？】
# 1. 编辑器支持：IDE（如 VSCode、PyCharm）可以提供智能代码补全
# 2. 类型检查：在运行前就能发现类型相关的错误
# 3. 自动文档：FastAPI 可以根据类型提示自动生成 API 文档
# 4. 开发体验：调用函数时，编辑器会提示参数类型和期望的输入
#
# 【传统写法 vs 类型提示写法】
# 传统写法（无类型提示）：
#   def get_full_name(first_name, last_name):
#       # 开发者可能忘记调用 .title() 方法
#       # 编辑器无法提供关于 first_name 和 last_name 的类型提示
#       full_name = first_name.title() + " " + last_name.title()
#       return full_name
#
# 类型提示写法（有类型提示）：
#   def get_full_name(first_name: str, last_name: str) -> str:
#       # 明确告诉编辑器 first_name 和 last_name 应该是字符串类型
#       # 调用时，编辑器会提示应该传递字符串类型的参数
#       # 如果传递了非字符串类型，编辑器会给出警告
#       full_name = first_name.title() + " " + last_name.title()
#       return full_name
#
# 【本示例的核心概念】
# - ": str" 表示参数应该是字符串类型
# - "-> str" 表示函数返回值应该是字符串类型
# - 当调用 get_full_name("john", "doe") 时，编辑器会正确提示字符串方法
# - title() 是字符串方法，将每个单词的首字母转换为大写


def get_full_name(first_name: str, last_name: str) -> str:
    """
    获取完整姓名

    Args:
        first_name: 名，字符串类型
        last_name: 姓，字符串类型

    Returns:
        完整姓名，格式为 "名 姓"，每个单词首字母大写
    """
    # 使用 title() 方法将每个单词的首字母转换为大写
    # "john".title() -> "John", "doe".title() -> "Doe"
    full_name = first_name.title() + " " + last_name.title()
    return full_name


# 测试函数调用
if __name__ == '__main__':
    result = get_full_name("john", "doe")
    print(result)  # 输出: John Doe
