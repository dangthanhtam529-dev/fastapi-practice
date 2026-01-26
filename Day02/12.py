# =============================================================================
# FastAPI 路径参数验证 - 使用 Path 类示例
# =============================================================================
# 本文件演示了如何使用 FastAPI 的 Path 类为路径参数添加验证规则和元数据
#
# 【Path 类】
# Path 类用于为路径参数添加验证规则和元数据，类似于 Query 类。
# 主要参数：
#   - ge: 大于等于（Greater than or Equal）
#   - gt: 大于（Greater than）
#   - le: 小于等于（Less than or Equal）
#   - lt: 小于（Less than）
#   - title: 标题
#   - description: 描述
#
# 【使用场景】
# 1. ID 验证：item_id 必须大于 0
# 2. 页码验证：page 必须大于等于 1
# 3. 数量验证：limit 必须大于 0


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI, Path  # FastAPI 和 Path 类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义路由，使用 Path 添加验证规则
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[
        int,  # 参数类型：整数
        Path(  # 路径参数验证器
            title="项目 ID",              # 参数标题（用于文档）
            description="要获取的项目 ID，必须是大于等于 1 的整数",
            ge=1,                        # 验证规则：大于等于 1
            # gt=0,                      # 可选：大于 0（不包括 0）
            # le=1000,                   # 可选：小于等于 1000
        )
    ],
    q: str  # 简单的查询参数，没有验证规则
):
    """
    根据 ID 获取项目信息

    演示如何使用 Path 类为路径参数添加验证规则

    Args:
        item_id: 项目 ID，整数类型，必须大于等于 1
        q: 可选的查询字符串

    Returns:
        dict: 包含项目 ID 和查询参数（如果有）的字典

    Examples:
        # 有效的项目 ID
        GET /items/1
        返回：{"item_id": 1}

        # 有效的项目 ID 和查询参数
        GET /items/1?q=test
        返回：{"item_id": 1, "q": "test"}

        # 无效的项目 ID（0）
        GET /items/0
        返回：422 错误（必须大于等于 1）

        # 无效的项目 ID（负数）
        GET /items/-1
        返回：422 错误（必须大于等于 1）

        # 无效的项目 ID（非数字）
        GET /items/abc
        返回：422 错误（不是有效的整数）
    """
    results = {"item_id": item_id}

    if q:
        results.update({"q": q})

    return results


# 【Path 类的验证参数】
# 数值验证（用于 int、float 类型）：
#   - ge: Greater than or Equal，大于等于
#   - gt: Greater than，大于
#   - le: Less than or Equal，小于等于
#   - lt: Less than，小于

# 字符串验证（用于 str 类型）：
#   - min_length: 最小长度
#   - max_length: 最大长度
#   - pattern: 正则表达式

# 元数据参数（用于所有类型）：
#   - title: 标题
#   - description: 描述
#   - alias: 别名


# 【验证失败示例】
# 请求：GET /items/0
# 返回 422 错误：
#   {
#       "detail": [
#           {
#               "type": "greater_than_equal",
#               "loc": ["path", "item_id"],
#               "msg": "Input should be greater than or equal to 1",
#               "input": 0,
#               "ctx": {"ge": 1},
#               "url": "https://errors.pydantic.dev/2.7/v/greater_than_equal"
#           }
#       ]
#   }


# 【多个路径参数的验证】
# @app.get("/users/{user_id}/items/{item_id}")
# async def read_items(
#     user_id: Annotated[int, Path(ge=1, title="用户 ID")],
#     item_id: Annotated[int, Path(ge=1, title="项目 ID")],
# ):


# 【测试方法】
# 1. 运行应用：uvicorn 12:app --reload
# 2. 访问 http://localhost:8000/docs
#    可以看到参数的验证规则
# 3. 尝试使用不同的 item_id 值进行测试


# 【实际应用场景】
# 1. 分页：/items/?page=1&size=10
#    page: Annotated[int, Path(ge=1)]
#    size: Annotated[int, Path(ge=1, le=100)]
#
# 2. ID 范围：/items/{item_id}
#    item_id: Annotated[int, Path(ge=1, le=10000)]
#
# 3. 版本号：/api/{version}
#    version: Annotated[str, Path(pattern=r'^v\d+$')]
