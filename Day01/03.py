# =============================================================================
# FastAPI 类型提示系统 - 泛型类型（列表）示例
# =============================================================================
# 本文件演示了 Python 类型提示中的泛型类型（Generic Types）
#
# 【什么是泛型类型？】
# 泛型类型是指包含一个或多个类型变量的类型。
# 在类型提示中，我们可以指定容器（如列表、字典）中元素的类型。
#
# 【列表类型提示】
# 使用 "list[元素类型]" 来表示一个元素类型为指定类型的列表：
#   list[str]        # 字符串列表
#   list[int]        # 整数列表
#   list[User]       # User 对象的列表（User 是自定义类）
#
# 【示例说明】
# - items: list[str] 表示 items 是一个字符串列表
# - 这样编辑器就知道列表中的每个元素都是字符串
# - 因此可以使用字符串的方法，如 .title(), .upper(), .lower() 等
#
# 【在 FastAPI 中的应用】
# 在 FastAPI 的路径操作函数中，我们可以使用泛型类型来定义请求体或响应：
#   @app.post("/items/")
#   async def create_items(items: list[str]):
#       # FastAPI 会验证请求体是一个字符串列表
#       for item in items:
#           process_item(item)
#       return {"items": items}


def process_items(items: list[str]) -> None:
    """
    处理字符串列表中的每个项目

    Args:
        items: 字符串列表，包含需要处理的项目名称

    Returns:
        无返回值，直接打印每个项目的标题格式
    """
    # 遍历列表中的每个字符串元素
    for item in items:
        # 使用 .title() 方法将每个单词首字母大写
        # "apple" -> "Apple", "banana" -> "Banana"
        print(item.title())


# 测试代码
if __name__ == '__main__':
    # 创建一个字符串列表
    items = ["apple", "banana", "orange"]

    # 调用处理函数
    process_items(items)

    # 输出结果：
    # Apple
    # Banana
    # Orange
