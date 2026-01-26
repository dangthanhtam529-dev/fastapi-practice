# =============================================================================
# FastAPI 数据模型 - 使用 Field 定义字段验证和元数据
# =============================================================================
# 本文件演示了如何使用 Pydantic 的 Field 类为模型字段添加验证规则和元数据
#
# 【Field 类的作用】
# Field 类用于在 Pydantic 模型中定义字段的：
# 1. 验证规则：如最小值、最大值、最小长度、最大长度
# 2. 描述信息：用于自动生成 API 文档
# 3. 默认值：字段的默认值
# 4. 其他元数据：如标题、示例值等
#
# 【Field 类的常用参数】
# - ... (省略号)：表示该字段是必需的（不能为 None 或省略）
# - default: 默认值
# - description: 字段描述（用于 API 文档）
# - title: 字段标题
# - min_length: 最小长度（用于字符串）
# - max_length: 最大长度（用于字符串）
# - ge: 大于等于（用于数字）
# - gt: 大于（用于数字）
# - le: 小于等于（用于数字）
# - lt: 小于（用于数字）
# - regex: 正则表达式（用于字符串）


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import Body, FastAPI  # FastAPI 框架
from pydantic import BaseModel, Field  # Pydantic 基类和 Field 类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义商品模型，使用 Field 添加验证规则和描述
class Item(BaseModel):
    """
    商品数据模型

    使用 Field 类为每个字段定义验证规则和描述信息，
    这些信息会自动反映在自动生成的 API 文档中。
    """
    # 使用 Field(..., description="...") 定义必需字段
    # 省略号 (...) 表示该字段是必需的，不能省略
    name: str = Field(
        ...,  # 省略号表示必需字段
        description="The name of the item",  # 字段描述
        min_length=1,  # 最小长度
        max_length=100  # 最大长度
    )

    # 使用 Field(None, description="...") 定义可选字段
    description: str | None = Field(
        None,  # 默认值为 None
        description="The description of the item",  # 字段描述
        max_length=500  # 最大长度
    )

    # 数值字段的验证
    price: float = Field(
        ...,  # 必需字段
        description="The price of the item",  # 字段描述
        gt=0,  # 必须大于 0（Greater than）
        le=1000000  # 必须小于等于 1000000（Less than or Equal）
    )

    # 可选的数值字段
    tax: float | None = Field(
        None,  # 默认值为 None
        description="The tax of the item",  # 字段描述
        ge=0,  # 必须大于等于 0
        le=100  # 必须小于等于 100
    )


# 定义更新路由
@app.put("/items/{item_id}")
async def create_item(
    item_id: int,  # 路径参数
    item: Annotated[
        Item,  # Pydantic 模型
        Body(
            embed=True  # 嵌入到请求体的 "item" 字段中
        )
    ]
):
    """
    创建或更新商品信息

    使用 Field 定义的验证规则会在请求体验证时自动应用

    Args:
        item_id: 商品 ID，路径参数
        item: 商品信息，请求体

    Returns:
        dict: 包含商品 ID 和商品信息的字典

    Examples:
        有效请求：
        PUT /items/123
        请求体：
        {
            "item": {
                "name": "Widget",
                "description": "A wonderful widget",
                "price": 19.99,
                "tax": 1.50
            }
        }

        无效请求（price 为负数）：
        PUT /items/123
        请求体：
        {
            "item": {
                "name": "Widget",
                "price": -5
            }
        }
        返回：422 错误
    """
    return {"item_id": item_id, "item": item}


# 【Field 验证失败示例】
# 请求：PUT /items/123
# 请求体：{"item": {"name": "W", "price": -5}}
#
# 返回 422 错误：
#   {
#       "detail": [
#           {
#               "type": "string_too_short",
#               "loc": ["body", "item", "name"],
#               "msg": "String should have at least 1 character",
#               "input": "W",
#               "ctx": {"min_length": 1},
#               "url": "..."
#           },
#           {
#               "type": "greater_than",
#               "loc": ["body", "item", "price"],
#               "msg": "Input should be greater than 0",
#               "input": -5,
#               "ctx": {"gt": 0},
#               "url": "..."
#           }
#       ]
#   }


# 【实际应用场景】
# 1. 用户注册：用户名、密码、邮箱的验证规则
# 2. 商品信息：价格、数量、描述的验证规则
# 3. 文章发布：标题、内容、标签的验证规则
# 4. 订单处理：数量、金额、地址的验证规则


# 【测试方法】
# 1. 运行应用：uvicorn 01:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看自动生成的 API 文档和字段验证规则
