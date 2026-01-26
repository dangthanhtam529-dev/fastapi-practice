# =============================================================================
# FastAPI 响应模型 - 使用返回类型注解示例
# =============================================================================
# 本文件演示了 FastAPI 的响应模型（Response Model）概念
#
# 【响应模型】
# 在 FastAPI 中，可以通过函数的返回类型注解来指定响应的数据结构。
# FastAPI 会：
# 1. 自动将返回值转换为指定的类型（通常是 Pydantic 模型）
# 2. 自动序列化为 JSON
# 3. 过滤掉不属于模型定义的字段
#
# 【三种定义响应模型的方式】
# 1. 函数返回类型注解：def create_item(item: Item) -> Item
# 2. response_model 参数：@app.post("/items/", response_model=Item)
# 3. 组合使用：def func() -> list[Item]
#
# 【为什么需要响应模型？】
# 1. 数据过滤：只返回需要的字段，隐藏敏感数据
# 2. 数据：将转换数据库对象转换为 API 响应格式
# 3. 类型安全：获得完整的类型检查支持
# 4. 自动文档：正确生成 OpenAPI 文档


# 导入 Pydantic
from pydantic import BaseModel

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


# 定义创建商品的路由
@app.post("/items/")
async def create_item(item: Item) -> Item:
    """
    创建新商品

    使用返回类型注解指定响应模型为 Item 类型

    Args:
        item: 商品信息，请求体

    Returns:
        Item: 创建的商品信息

    Note:
        返回的 Item 会自动转换为 JSON 响应
    """
    return item


# 定义获取商品列表的路由
@app.get("/items/")
async def read_items() -> list[Item]:
    """
    获取商品列表

    使用返回类型注解指定响应模型为 Item 列表

    Returns:
        list[Item]: 商品列表

    Note:
        返回的列表会自动转换为 JSON 数组格式
    """
    # 返回 Item 对象列表
    # FastAPI 会自动将其转换为 JSON 数组
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


# 【响应模型的作用】
# 1. 数据过滤示例：
#    如果返回的字典包含 extra 字段，使用响应模型会自动过滤：
#    def create_item(item: Item) -> Item:
#        # 假设我们有额外的 internal_id 字段
#        return {"name": item.name, "internal_id": 123}
#    # 响应只包含 name 字段，internal_id 被过滤

# 2. 隐藏敏感数据：
#    class User(BaseModel):
#        username: str
#        password: str  # 敏感字段
#
#    @app.get("/users/", response_model=list[UserOut])
#    async def get_users() -> list[User]:
#        users = db.get_all_users()
#        return users
#    # UserOut 不包含 password，响应中不会泄露密码


# 【实际应用场景】
# 1. 创建操作：返回创建的完整对象
# 2. 列表操作：返回对象列表
# 3. 详情操作：返回单个对象的详细信息
# 4. 摘要操作：返回对象的部分字段


# 【测试方法】
# 1. 运行应用：uvicorn 04:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看 API 文档中的响应模型
