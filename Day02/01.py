# =============================================================================
# FastAPI 路径参数 - 基础类型路径参数示例
# =============================================================================
# 本文件演示了 FastAPI 中路径参数（Path Parameters）的基本用法
#
# 【什么是路径参数？】
# 路径参数是 URL 路径中的一部分，用于动态传递值给 API。
# 例如：/item/123 中的 "123" 就是一个路径参数。
#
# 【定义路径参数】
# 在 FastAPI 中，使用 "{参数名}" 的语法在路径中定义路径参数：
#   @app.get("/item/{item_id}")
#
# 然后在路径操作函数中添加同名参数，FastAPI 会自动提取并转换该参数：
#   async def read_item(item_id: int):
#       # FastAPI 会自动将 URL 中的 "item_id" 值传递给函数参数
#
# 【路径参数的类型】
# 可以为路径参数指定类型提示，FastAPI 会自动进行类型转换和验证：
#   item_id: int     # 整数类型，如 /item/123
#   item_id: str     # 字符串类型，如 /item/abc
#   item_id: float   # 浮点数类型，如 /item/3.14
#
# 【类型转换和验证】
# 如果路径参数指定了类型，FastAPI 会：
# 1. 自动将 URL 中的字符串转换为指定的类型
# 2. 如果转换失败，返回 422 错误（数据验证失败）
# 3. 如果类型正确，继续处理请求
#
# 【示例说明】
# - 访问 /item/123 时，item_id = 123（整数）
# - 访问 /item/abc 时，如果类型是 int，会返回 422 错误
# - 访问 /item/3.14 时，如果类型是 float，item_id = 3.14


# 导入 FastAPI
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义带路径参数的 GET 请求
# 路径中的 {item_id} 是一个占位符，表示这是动态参数
# 访问 /item/123、/item/456 等都会匹配这个路由
@app.get("/item/{item_id}")
async def read_root(item_id: int):
    """
    根据 ID 获取项目信息

    Args:
        item_id: 项目 ID，整数类型

    Returns:
        dict: 包含项目 ID 的字典

    Raises:
        HTTPException: 如果 item_id 不是有效的整数，返回 422 错误
    """
    # FastAPI 自动将路径参数 item_id 转换为整数
    # 返回一个包含 item_id 的字典，FastAPI 会自动序列化为 JSON
    return {"item_id": item_id}


# 【测试方法】
# 1. 运行应用：uvicorn 01:app --reload
# 2. 访问 http://localhost:8000/item/123
#    返回：{"item_id":123}
# 3. 访问 http://localhost:8000/item/abc
#    返回：422 错误（无法将 "abc" 转换为整数）
# 4. 访问 http://localhost:8000/docs 查看自动生成的 API 文档


# 【路径参数的实际应用场景】
# - 获取特定用户信息：/users/{user_id}
# - 获取特定商品信息：/products/{product_id}
# - 获取特定订单详情：/orders/{order_id}
# - 获取特定文章内容：/articles/{article_id}
