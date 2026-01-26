# =============================================================================
# FastAPI 数据模型 - 使用 model_config 自定义 JSON Schema 示例
# =============================================================================
# 本文件演示了如何使用 Pydantic 的 model_config 配置模型的行为和元数据
#
# 【model_config】
# model_config 是 Pydantic 模型的一个配置字典，用于自定义模型的行为和元数据。
# 常用配置项：
#   - json_schema_extra: 自定义 JSON Schema 和示例数据
#   - from_attributes: 是否从对象属性创建模型
#   - populate_by_name: 是否允许使用别名填充字段
#   - extra: 控制额外字段的行为（"allow", "forbid", "ignore"）
#
# 【json_schema_extra】
# 用于在自动生成的 JSON Schema 中添加额外的元数据：
#   - examples: 示例值，帮助 API 文档使用者理解请求格式
#   - description: 额外的描述信息
#   - default: 默认值信息


# 导入 Pydantic
from pydantic import BaseModel

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义商品模型，使用 model_config 配置示例数据
class Item(BaseModel):
    """
    商品数据模型

    使用 model_config 自定义 JSON Schema 和示例数据，
    这些示例会自动显示在自动生成的 API 文档中。
    """
    # 基本字段
    name: str           # 必需字段：商品名称
    description: str | None = None  # 可选字段：商品描述
    price: float        # 必需字段：商品价格
    tax: float | None = None  # 可选字段：商品税费

    # 模型配置
    model_config = {
        # 自定义 JSON Schema 的额外内容
        "json_schema_extra": {
            # 示例值数组，帮助 API 文档使用者理解请求格式
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                # 可以添加多个示例
                {
                    "name": "Bar",
                    "description": "Another great item",
                    "price": 25.0,
                    # tax 字段是可选的，可以省略
                }
            ]
        }
    }


# 定义更新路由
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,  # 路径参数
    item: Item     # 请求体
):
    """
    更新商品信息

    Item 模型的示例会自动显示在 API 文档中

    Args:
        item_id: 商品 ID，路径参数
        item: 商品信息，请求体

    Returns:
        dict: 包含商品 ID 和商品信息的字典

    Examples:
        可以参考 Item 模型中定义的 examples
    """
    results = {"item_id": item_id, "item": item}
    return results


# 【model_config 的其他配置项】
# 1. 控制额外字段：
#    model_config = {"extra": "forbid"}  # 禁止额外字段
#    model_config = {"extra": "ignore"}  # 忽略额外字段
#    model_config = {"extra": "allow"}   # 允许额外字段

# 2. 从对象属性创建模型：
#    from pydantic import BaseModel
#
#    class User:
#        def __init__(self, name: str, age: int):
#            self.name = name
#            self.age = age
#
#    class Item(BaseModel):
#        model_config = {"from_attributes": True}
#
#    user = User("John", 25)
#    item = Item.model_validate(user)  # 从对象创建模型实例


# 【使用 curl 测试】
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{"name": "Widget", "price": 19.99}'


# 【实际应用场景】
# 1. API 文档：提供清晰的示例帮助前端开发者
# 2. 数据验证：为复杂的验证规则提供文档
# 3. 默认值：定义字段的预期行为
# 4. 业务规则：描述业务逻辑的限制


# 【测试方法】
# 1. 运行应用：uvicorn 06:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看 Item 模型的示例数据
