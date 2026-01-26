# =============================================================================
# FastAPI 查询参数验证 - 使用 Annotated 和 Query 示例
# =============================================================================
# 本文件演示了如何使用 Python 的 Annotated 和 FastAPI 的 Query 类
# 为查询参数添加验证规则
#
# 【为什么要验证查询参数？】
# 查询参数虽然通常是可选的，但有时需要：
# 1. 限制长度（如搜索关键词至少3个字符）
# 2. 限制范围（如页码必须大于0）
# 3. 正则匹配（如只允许字母数字）
#
# 【Annotated】
# Python 3.9+ 引入了 Annotated 类型，用于添加元数据。
# 格式：Annotated[类型, 元数据...]
#
# 【Query 类】
# FastAPI 的 Query 类用于为查询参数添加验证规则和元数据。
# 主要参数：
#   - default: 默认值
#   - min_length: 最小长度
#   - max_length: 最大长度
#   - pattern: 正则表达式
#   - alias: 参数别名
#   - title: 标题
#   - description: 描述


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI, Query  # FastAPI 和 Query 类

# 创建 FastAPI 应用实例
app = FastAPI()


# 使用 Annotated 和 Query 添加验证规则
# q: Annotated[str | None, Query(...)] = None
#   - str | None: 参数类型是字符串或 None
#   - Query(min_length=3, max_length=50): 验证规则
#   - = None: 默认值
@app.get("/items/")
async def read_items(
    # Annotated 的第二个参数是元数据，这里使用 Query 定义验证规则
    q: Annotated[
        str | None,  # 参数类型
        Query(       # 查询参数验证器
            min_length=3,   # 最小长度 3 个字符
            max_length=50,  # 最大长度 50 个字符
            # pattern=r"^[a-zA-Z0-9]+$",  # 可以添加正则表达式限制
            title="搜索关键词",
            description="搜索商品的关键词，至少3个字符，最多50个字符"
        )
    ] = None
):
    """
    获取商品列表，支持搜索过滤

    Args:
        q: 搜索关键词，可选参数。
           - 最小长度：3 个字符
           - 最大长度：50 个字符
           - 如果不提供或为空，返回所有商品
           - 如果提供，返回匹配的商品

    Returns:
        dict: 包含商品列表和搜索关键词（如果有）的字典

    Examples:
        # 不使用搜索
        GET /items/
        返回：{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}

        # 使用搜索（关键词符合长度要求）
        GET /items/?q=apple
        返回：{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}], "q": "apple"}

        # 使用搜索（关键词太短）
        GET /items/?q=ab
        返回：422 错误（验证失败）

        # 使用搜索（关键词太长）
        GET /items/?q=abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz
        返回：422 错误（验证失败）
    """
    # 基础响应
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}

    # 如果提供了搜索关键词，添加到响应中
    if q:
        results.update({"q": q})

    return results


# 【Query 类的其他常用参数】
#   - default: 默认值，如 Query(default=None)
#   - alias: 参数别名，如 Query(alias="keyword")，则使用 ?keyword= 而不是 ?q=
#   - deprecated: 标记参数已废弃，如 Query(deprecated=True)
#   - include_in_schema: 是否在文档中显示，如 Query(include_in_schema=False)


# 【验证失败的处理】
# 如果查询参数不满足验证条件，FastAPI 会自动返回 422 错误：
#   {
#       "detail": [
#           {
#               "type": "string_too_short",
#               "loc": ["query", "q"],
//               "msg": "String should have at least 3 characters",
//               "input": "ab",
//               "url": "https://errors.pydantic.dev/2.7/v/string_too_short"
//           }
//       ]
//   }


# 【测试方法】
# 1. 运行应用：uvicorn 09:app --reload
# 2. 访问 http://localhost:8000/docs
#    可以看到参数的验证规则
# 3. 尝试使用不同长度的搜索关键词
