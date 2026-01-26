# =============================================================================
# FastAPI 类型提示系统 - 泛型类型（字典）示例
# =============================================================================
# 本文件演示了 Python 类型提示中的字典类型提示
#
# 【字典类型提示】
# 使用 "dict[键类型, 值类型]" 来表示一个字典及其键值对的类型：
#   dict[str, int]      # 键是字符串，值是整数的字典
#   dict[str, float]    # 键是字符串，值是浮点数的字典
#   dict[str, any]      # 键是字符串，值是任意类型的字典
#
# 【类型 any】
# "any" 类型表示值可以是任何类型，相当于类型提示中的 "object"
# 在 Python 中，any 等同于不指定类型，但语义上更清晰
#
# 【示例说明】
# - items: dict[str, any] 表示 items 是一个字典
# - 字典的键（key）必须是字符串类型
# - 字典的值（value）可以是任何类型
#
# 【在 FastAPI 中的应用】
# 在 FastAPI 中，字典类型提示常用于：
# 1. 请求体：接收前端发送的 JSON 数据
# 2. 响应体：返回灵活的 JSON 数据结构
#
# 示例：
#   @app.post("/process/")
#   async def process_data(data: dict[str, any]):
#       # FastAPI 会验证请求体是一个字典
#       # 字典的键是字符串，值可以是任何类型
#       return {"processed": data}


def process_items(items: dict[str, any]) -> None:
    """
    处理字典中的所有键值对

    Args:
        items: 字典，键为字符串类型，值为任意类型

    Returns:
        无返回值，直接打印每个键值对
    """
    # 使用 .items() 方法遍历字典的所有键值对
    for key, value in items.items():
        # 将键的首字母转换为大写，然后打印键和值
        # key.title() 将键转换为标题格式
        print(key.title(), value)


# 测试代码
if __name__ == '__main__':
    # 创建一个字典，键是字符串，值是整数
    items = {"apple": 1, "banana": 2, "orange": 3}

    # 调用处理函数
    process_items(items)

    # 输出结果：
    # Apple 1
    # Banana 2
    # Orange 3

    # 也可以处理值类型不同的字典
    mixed_items = {
        "name": "Alice",
        "age": 25,
        "height": 5.6,
        "is_student": True
    }
    process_items(mixed_items)

    # 输出结果：
    # Name Alice
    # Age 25
    # Height 5.6
    # Is Student True
