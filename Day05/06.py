# =============================================================================
# FastAPI 响应模型 - 使用不同输入输出模型过滤敏感数据示例
# =============================================================================
# 本文件演示了如何使用不同的输入模型和输出模型来过滤敏感数据
#
# 【为什么使用不同的输入输出模型？】
# 在实际应用中，我们经常需要：
# 1. 接收完整的数据（包括敏感信息如密码）
# 2. 返回过滤后的数据（不包含敏感信息）
#
# 这种模式可以保护用户隐私，防止敏感数据泄露。
#
# 【EmailStr 类型】
# EmailStr 是 Pydantic 提供的特殊类型，用于验证电子邮件地址格式。
# 它会自动验证输入是否是有效的电子邮件格式。


# 导入必要的模块
from typing import Any  # 用于表示任意类型

from fastapi import FastAPI  # FastAPI 框架
from pydantic import BaseModel, EmailStr  # Pydantic 基类和 EmailStr 类型

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义用户输入模型（包含敏感信息）
class UserIn(BaseModel):
    """
    用户输入模型

    用于接收用户注册信息，包含敏感字段 password

    Attributes:
        username: 用户名
        password: 密码（敏感字段）
        email: 电子邮件地址
        full_name: 全名（可选）
    """
    username: str     # 必需：用户名
    password: str     # 必需：密码（敏感信息）
    email: EmailStr   # 必需：电子邮件地址（自动验证格式）
    full_name: str | None = None  # 可选：全名


# 定义用户输出模型（不包含敏感信息）
class UserOut(BaseModel):
    """
    用户输出模型

    用于返回用户信息，不包含敏感字段 password

    Attributes:
        username: 用户名
        email: 电子邮件地址
        full_name: 全名（可选）
    """
    username: str     # 用户名
    email: EmailStr   # 电子邮件地址
    full_name: str | None = None  # 可选：全名
    # 注意：password 字段被排除，不会在响应中返回


# 定义创建用户的路由
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    """
    创建新用户

    演示使用不同的输入输出模型：
    - 输入：UserIn（包含密码）
    - 输出：UserOut（不包含密码）

    Args:
        user: 用户信息，包含敏感密码

    Returns:
        UserOut: 用户信息，不包含密码

    Note:
        即使输入模型包含密码，响应模型也会过滤掉，
        确保密码不会泄露给客户端。
    """
    # 假设这里会进行密码加密等处理
    # stored_user = hash_password(user.password)
    # ...

    # 返回用户信息，但 password 会被 response_model 过滤
    return user


# 【EmailStr 验证示例】
# 有效的电子邮件：
#   "user@example.com"
#   "user.name@example.com"
#   "user+tag@example.com"

# 无效的电子邮件：
#   "not-an-email"
#   "@example.com"
#   "user@"
#   "user@example"


# 【实际应用场景】
# 1. 用户注册：接收密码，返回用户信息
# 2. 用户更新：接收完整信息，返回更新后的信息
# 3. 登录认证：接收凭据，返回令牌
# 4. 个人信息查询：返回公开信息，隐藏敏感信息


# 【安全最佳实践】
# 1. 永远不要在响应中返回密码
# 2. 使用 HTTPS 传输敏感数据
# 3. 对密码进行加密存储
# 4. 使用强密码策略


# 【测试方法】
# 1. 运行应用：uvicorn 06:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 尝试创建用户，查看响应是否包含密码字段
