# =============================================================================
# FastAPI 响应模型 - 使用 response_model 参数示例
# =============================================================================
# 本文件演示了如何使用 FastAPI 的 response_model 参数显式指定响应模型
#
# 【response_model 参数】
# 在路径操作装饰器中使用 response_model 参数来指定响应的数据结构：
#   @app.post("/items/", response_model=Item)
#
# 【为什么需要 response_model？】
# 有时函数的实际返回类型与期望的响应类型不同：
# 1. 函数使用 -> Any 避免类型检查
# 2. 返回的是字典而不是 Pydantic 模型对象
# 3. 需要从数据库对象转换到 API 响应格式
#
# 【response_model 的作用】
# 1. 指定期望的响应数据结构
# 2. 自动过滤不属于响应模型的字段
# 3. 自动生成正确的 OpenAPI 文档
# 4. 提供正确的 JSON Schema


# 导入必要的模块
from typing import Any  # 用于表示任意类型

from fastapi import FastAPI  # FastAPI 框架
from pydantic import BaseModel  # Pydantic 基类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义商品数据模型
class Item(BaseModel):
    """
    商品数据模型

    Attributes:
        name: 商品名称
        description: 商品描述（可选）
        price: 商品价格
        tax: 税费（可选）
        tags: 商品标签列表
    """
    name: str                      # 必需：商品名称
    description: str | None = None # 可选：商品描述
    price: float                   # 必需：商品价格
    tax: float | None = None       # 可选：商品税费
    tags: list[str] = []           # 可选：商品标签列表


# 定义创建商品的路由，使用 response_model 参数
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    """
    创建新商品

    使用 response_model 参数显式指定响应模型为 Item

    Args:
        item: 商品信息，请求体

    Returns:
        Item: 符合 Item 模型的数据

    Note:
        虽然函数返回类型是 Any，但 response_model=Item 确保
        响应符合 Item 模型的结构，并自动进行数据过滤。
    """
    # 假设这里有一些额外的处理逻辑
    # 返回 Item 对象，但响应会根据 response_model 过滤
    return item


# 定义获取商品列表的路由，使用 response_model 参数
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    """
    获取商品列表

    使用 response_model=list[Item] 指定响应模型为 Item 列表

    Returns:
        list[Item]: 符合 Item 模型的商品列表

    Note:
        即使返回的是字典列表，response_model=list[Item] 会确保
        每个字典都符合 Item 模型的结构。
    """
    # 返回字典列表（不是 Item 对象列表）
    # response_model 会自动处理转换和过滤
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# 【response_model vs 返回类型注解】
# response_model 参数：
#   - 显式指定响应的数据结构
#   - 优先于返回类型注解
#   - 用于过滤和验证响应数据

# 返回类型注解（-> Item）：
#   - 提供类型检查支持
#   - IDE 代码补全
#   - 文档生成

# 建议：同时使用两者以获得最佳开发体验


# 【实际应用场景】
# 1. 数据库对象转换：
#    @app.get("/users/{user_id}", response_model=UserOut)
#    async def get_user(user_id: int) -> Any:
#        user = db.get_user(user_id)  # 返回数据库模型
#        return user  # response_model 会转换为 API 响应格式

# 2. 过滤敏感数据：
#    class User(BaseModel):
#        username: str
#        password: str  # 敏感字段
#
#    @app.get("/users/", response_model=UserPublic)
#    async def get_users() -> Any:
#        users = db.get_all_users()  # 返回包含密码的用户列表
#        return users  # response_model 会过滤掉密码


# 【测试方法】
# 1. 运行应用：uvicorn 05:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看 API 文档中的响应模型
