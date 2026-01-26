# =============================================================================
# FastAPI 混合参数类型示例 - 路径参数 + 查询参数 + 请求体
# =============================================================================
# 本文件演示了如何在同一个路由中同时使用多种类型的参数
#
# 【参数类型概述】
# FastAPI 支持以下类型的参数：
# 1. 路径参数：在 URL 路径中，如 /items/{item_id}
# 2. 查询参数：在 URL ? 后面，如 ?q=keyword
# 3. 请求体：JSON 数据，如 {"name": "item", "age": 10}
# 4. 请求头：HTTP 请求头，如 Authorization: Bearer xxx
# 5. Cookie：HTTP Cookie
#
# 【参数声明规则】
# FastAPI 会根据参数的类型提示自动识别参数类型：
# - 在路径中有对应 {param} 的 → 路径参数
# - 有默认值或默认值不是 Path/Query/Body 的 → 查询参数
# - 类型是 Pydantic 模型 → 请求体
# - 使用 Path/Query/Body 等装饰器 → 显式指定类型


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型
from pydantic import BaseModel  # Pydantic 基类
from fastapi import FastAPI, Query, Path  # FastAPI 框架和参数验证器

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义请求体模型
class Item(BaseModel):
    """
    项目数据模型

    Attributes:
        name: 项目名称，字符串类型，必填
        age: 项目年龄，整数类型，必填
    """
    name: str  # 必需字段：项目名称
    age: int   # 必需字段：项目年龄


# 定义 PUT 路由，同时使用多种参数类型
@app.put("/items/{item_id}")
async def read_root(
    item_id: Annotated[
        int,  # 参数类型：整数
        Path(
            title="项目 ID",  # 参数标题
            ge=1  # 验证规则：必须大于等于 1
        )
    ],
    q: str,      # 查询参数：q 是可选的查询字符串
    item: Item   # 请求体：Item 模型实例
):
    """
    更新指定项目的信息

    这个示例展示了如何在同一个路由中混合使用：
    - 路径参数 (item_id)：标识要更新的项目
    - 查询参数 (q)：可选的搜索或过滤条件
    - 请求体 (item)：要更新的数据

    Args:
        item_id: 项目 ID，路径参数，必须大于等于 1
        q: 查询字符串，可选参数
        item: 项目数据，请求体

    Returns:
        dict: 包含所有参数的字典

    Examples:
        # 完整请求
        PUT /items/123?q=search
        请求体：{"name": "Updated Item", "age": 10}
        返回：{"item_id": 123, "q": "search", "item": {"name": "Updated Item", "age": 10}}

        # 简单请求
        PUT /items/1
        请求体：{"name": "Item", "age": 5}
        返回：{"item_id": 1, "q": null, "item": {"name": "Item", "age": 5}}
    """
    # 构建响应
    result = {
        "item_id": item_id,  # 路径参数
        "q": q,              # 查询参数
        "item": item         # 请求体
    }

    return result


# 【参数类型识别说明】
# FastAPI 根据以下规则自动识别参数类型：

# 1. 路径参数：路径中有 {param}，如 /items/{item_id}
#    item_id: int → 自动识别为路径参数

# 2. 查询参数：在 ? 后面，没有在路径中定义
#    q: str → 自动识别为查询参数

# 3. 请求体：类型是 Pydantic 模型
#    item: Item → 自动识别为请求体


# 【使用场景】
# 1. 更新资源：PUT /items/{item_id} + 请求体
# 2. 带搜索的更新：PUT /items/{item_id}?q=keyword + 请求体
# 3. 带验证的更新：PUT /items/{item_id} + 验证后的请求体


# 【测试方法】
# 1. 运行应用：uvicorn 02:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 尝试不同的参数组合
