# =============================================================================
# FastAPI 参数验证 - 使用 AfterValidator 自定义验证示例
# =============================================================================
# 本文件演示了如何使用 Pydantic 的 AfterValidator 进行自定义参数验证
#
# 【AfterValidator】
# AfterValidator 是 Pydantic 提供的验证器之一，它在类型转换后运行自定义验证逻辑。
# 适用于需要复杂验证规则的场景。
#
# 【验证器类型】
# - BeforeValidator: 在类型转换之前运行
# - AfterValidator: 在类型转换之后运行（本案列使用）
# - WrapValidator: 可以控制验证流程
#
# 【使用场景】
# 1. 格式验证（如 ID 必须以特定前缀开头）
# 2. 范围验证（如数值必须在特定范围内）
# 3. 业务逻辑验证（如用户名不能包含特定字符）


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI  # FastAPI 框架
from pydantic import AfterValidator  # 后置验证器

# 导入 random 模块用于随机选择
import random

# 创建 FastAPI 应用实例
app = FastAPI()


# 模拟数据存储
# 键是符合特定格式的 ID，值是对应的名称
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


# 自定义验证函数
# 这个函数在类型转换后运行，用于验证 ID 格式
def check_valid_id(id: str) -> str:
    """
    验证 ID 格式

    Args:
        id: 需要验证的 ID 字符串

    Returns:
        str: 验证通过的 ID

    Raises:
        ValueError: 如果 ID 格式不正确
    """
    # 检查 ID 是否以 "isbn-" 或 "imdb-" 开头
    if not id.startswith(("isbn-", "imdb-")):
        # 如果格式不正确，抛出 ValueError
        raise ValueError(
            'Invalid ID format, it must start with "isbn-" or "imdb-"'
        )
    return id


# 定义路由，使用 AfterValidator 进行自定义验证
@app.get("/items/")
async def read_items(
    id: Annotated[
        str | None,                    # 参数类型：字符串或 None
        AfterValidator(check_valid_id) # 后置验证器
    ] = None
):
    """
    根据 ID 获取项目信息

    如果提供了 ID，验证其格式后返回对应项目；
    如果未提供 ID，随机返回一个项目。

    Args:
        id: 项目 ID，可选参数。
            - 必须以 "isbn-" 或 "imdb-" 开头
            - 如果格式不正确，返回 422 错误

    Returns:
        dict: 包含 ID 和项目名称的字典

    Examples:
        # 提供有效的 ID
        GET /items/?id=isbn-9781529046137
        返回：{"id": "isbn-9781529046137", "name": "The Hitchhiker's Guide..."}

        # 提供无效的 ID
        GET /items/?id=invalid-id
        返回：422 错误（验证失败）

        # 不提供 ID（随机返回）
        GET /items/
        返回：{"id": "imdb-tt0371724", "name": "The Hitchhiker's Guide..."}
    """
    if id:
        # 如果提供了 ID，从数据中获取对应项目
        item = data.get(id)
    else:
        # 如果没有提供 ID，随机选择一个项目
        id, item = random.choice(list(data.items()))

    return {"id": id, "name": item}


# 【AfterValidator 的工作流程】
# 1. 客户端发送请求：/items/?id=isbn-123
# 2. FastAPI 提取查询参数：id = "isbn-123"
# 3. 类型转换：str 类型，无需转换
# 4. AfterValidator 调用 check_valid_id("isbn-123")
# 5. 验证通过，返回 "isbn-123"
# 6. 调用 read_items 函数

# 【验证失败的情况】
# 1. 客户端发送：/items/?id=invalid-id
# 2. AfterValidator 调用 check_valid_id("invalid-id")
# 3. 检查失败，抛出 ValueError
# 4. FastAPI 返回 422 错误：
#    {
#        "detail": [
#            {
#                "type": "value_error",
#                "loc": ["query", "id"],
#                "msg": "Value error, Invalid ID format..."
#            }
#        ]
#    }


# 【测试方法】
# 1. 运行应用：uvicorn 11:app --reload
# 2. 访问 http://localhost:8000/items/?id=isbn-9781529046137
#    返回有效的项目信息
# 3. 访问 http://localhost:8000/items/?id=invalid
#    返回 422 错误
# 4. 访问 http://localhost:8000/items/
#    返回随机项目


# 【其他验证器的使用场景】
# - BeforeValidator: 需要在类型转换前处理的验证
# - WrapValidator: 需要访问验证上下文的复杂验证
# - Field: 用于 Pydantic 模型字段的验证
