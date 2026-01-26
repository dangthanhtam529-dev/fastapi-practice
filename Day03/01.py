# =============================================================================
# FastAPI 查询参数 - 使用 Pydantic 模型作为查询参数示例
# =============================================================================
# 本文件演示了如何将 Pydantic 模型与查询参数结合使用
#
# 【为什么使用 Pydantic 模型作为查询参数？】
# 1. 复杂的验证逻辑：将多个查询参数的验证规则集中在一个模型中
# 2. 代码复用：可以在多个路由中复用同一个查询模型
# 3. 清晰的文档：自动生成清晰的 API 文档
# 4. 更好的类型支持：获得完整的 IDE 代码补全支持
#
# 【model_config 配置】
# model_config 是 Pydantic 模型的一个配置字典，常用选项：
#   - "extra": 控制额外字段的行为
#     * "forbid": 禁止额外字段（如果提供则报错）
#     * "ignore": 忽略额外字段
#     * "allow": 允许额外字段
#   - "json_schema_extra": 定义 JSON Schema 元数据


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI, Query  # FastAPI 框架和查询参数验证器
from pydantic import BaseModel  # Pydantic 基类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义查询参数模型
# 这个模型定义了查询参数的结构和验证规则
class Filter(BaseModel):
    """
    过滤器查询参数模型

    用于验证查询参数，包含以下字段：
    - name: 名称过滤条件（可选）
    - age: 年龄过滤条件（可选）

    配置：
    - extra="forbid": 禁止额外的查询参数
    """
    model_config = {
        "extra": "forbid"  # 禁止接收模型中未定义的字段
    }

    name: str | None = None  # 可选的名称过滤条件
    age: int | None = None   # 可选的年龄过滤条件


# 定义使用 Pydantic 模型作为查询参数的路由
# filter_query: Annotated[Filter, Query()]
#   - Filter: 查询参数的类型是 Filter 模型
#   - Query(): 使用查询参数验证器
#   - 参数名 filter_query 会成为 URL 中的查询参数名
@app.get("/items/")
async def read_root(
    filter_query: Annotated[
        Filter,   # 查询参数类型
        Query()   # 查询参数验证器
    ]
):
    """
    获取项目列表，支持过滤

    使用 Pydantic 模型作为查询参数，可以实现复杂的过滤逻辑

    Args:
        filter_query: Filter 模型实例，包含过滤条件

    Returns:
        Filter: 返回过滤条件本身（实际应用中通常用于数据库查询）

    Examples:
        # 不使用过滤
        GET /items/
        返回：{"name": null, "age": null}

        # 使用名称过滤
        GET /items/?name=John
        返回：{"name": "John", "age": null}

        # 使用年龄过滤
        GET /items/?age=25
        返回：{"name": null, "age": 25}

        # 组合过滤
        GET /items/?name=John&age=25
        返回：{"name": "John", "age": 25}

        # 使用额外参数（会被拒绝）
        GET /items/?name=John&extra=xxx
        返回：422 错误（extra 字段被禁止）
    """
    return filter_query


# 【Pydantic 模型作为查询参数 vs 普通参数】
# 普通参数方式：
#   @app.get("/items/")
#   async def read_items(name: str | None = None, age: int | None = None):
#       ...

# 模型方式的优势：
# 1. 验证规则集中管理
# 2. 可以使用 model_config 配置
# 3. 易于扩展和复用
# 4. 文档更加清晰


# 【实际应用场景】
# 1. 复杂搜索：@app.get("/search/")，search: Annotated[SearchQuery, Query()]
# 2. 高级过滤：@app.get("/products/")，filter: Annotated[ProductFilter, Query()]
# 3. 分页参数：@app.get("/items/")，pagination: Annotated[PaginationParams, Query()]


# 【测试方法】
# 1. 运行应用：uvicorn 01:app --reload
# 2. 访问 http://localhost:8000/docs
#    查看自动生成的 API 文档
# 3. 尝试使用不同的查询参数组合
