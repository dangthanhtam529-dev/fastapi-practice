# =============================================================================
# FastAPI 请求体 - Pydantic BaseModel 基础示例
# =============================================================================
# 本文件演示了如何使用 Pydantic 的 BaseModel 定义请求体
#
# 【什么是请求体？】
# 请求体是客户端发送给服务器的 JSON 数据，通常用于：
# 1. 创建新资源（POST 请求）
# 2. 更新现有资源（PUT/PATCH 请求）
#
# 【Pydantic 简介】
# Pydantic 是一个 Python 数据验证和设置管理库。
# 它使用 Python 类型提示来验证数据，并提供自动补全支持。
#
# 【BaseModel 的作用】
# 1. 数据验证：自动验证请求体中的数据类型
# 2. 类型转换：自动将 JSON 数据转换为 Python 类型
# 3. 文档生成：FastAPI 自动根据模型生成 API 文档
# 4. IDE 支持：提供完整的代码补全和类型检查
#
# 【字段类型】
# - str: 字符串类型
# - int: 整数类型
# - float: 浮点数类型
# - bool: 布尔类型
# - None: 可空类型
# - X | None: 联合类型（X 类型或 None）


# 导入 FastAPI 和 Pydantic
from fastapi import FastAPI
from pydantic import BaseModel

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义数据模型
# Item 继承自 BaseModel，用于描述请求体/响应体的结构
class Item(BaseModel):
    """
    商品数据模型

    用于定义商品的 JSON 结构，包含以下字段：
    - name: 商品名称（必需）
    - description: 商品描述（可选，默认 None）
    - price: 商品价格（必需）
    - tax: 税费（可选，默认 None）

    Attributes:
        name: 商品名称，字符串类型，必填
        description: 商品描述，字符串类型，可选
        price: 商品价格，浮点数类型，必填
        tax: 商品税费，浮点数类型，可选
    """
    name: str                       # 必需字段：商品名称
    description: str | None = None  # 可选字段：商品描述，默认 None
    price: float                    # 必需字段：商品价格
    tax: float | None = None        # 可选字段：商品税费，默认 None


# 创建商品的 POST 路由
# 当客户端发送 POST 请求到 /items/ 时，FastAPI 会：
# 1. 解析请求体中的 JSON 数据
# 2. 使用 Item 模型验证数据
# 3. 如果数据无效，返回 422 错误
# 4. 如果数据有效，将数据传递给 create_item 函数
@app.post("/items/")
async def create_item(item: Item):
    """
    创建新商品

    接收商品信息，验证后返回创建的商品

    Args:
        item: Item 对象，包含商品信息

    Returns:
        Item: 创建的商品对象，FastAPI 会自动转换为 JSON 响应

    Raises:
        HTTPException: 如果请求体无效，返回 422 错误

    Example:
        请求体：
        {
            "name": "Widget",
            "description": "A wonderful widget",
            "price": 19.99,
            "tax": 1.50
        }

        响应：
        {
            "name": "Widget",
            "description": "A wonderful widget",
            "price": 19.99,
            "tax": 1.50
        }
    """
    return item


# 【Pydantic 自动验证示例】
# 如果发送的请求体不符合模型定义，FastAPI 会自动返回错误：

# 无效请求（缺少必需的 name 字段）：
#   POST /items/
#   {"price": 19.99}
# 返回：422 Unprocessable Entity

# 无效请求（price 不是数字）：
#   POST /items/
#   {"name": "Widget", "price": "expensive"}
# 返回：422 Unprocessable Entity

# 有效请求：
#   POST /items/
#   {"name": "Widget", "price": 19.99}
# 返回：{"name": "Widget", "price": 19.99, "description": null, "tax": null}


# 【测试方法】
# 1. 运行应用：uvicorn 08:app --reload
# 2. 访问 http://localhost:8000/docs
#    可以看到自动生成的 Swagger UI 文档
# 3. 在文档中尝试创建商品
#    Pydantic 会自动验证输入数据


# 【Pydantic 的优势】
# 1. 类型安全：在运行前捕获类型错误
# 2. 自动补全：IDE 可以提供代码补全
# 3. 清晰定义：数据模型一目了然
# 4. 易于维护：修改模型即可改变验证规则
