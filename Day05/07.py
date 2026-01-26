# =============================================================================
# FastAPI 响应模型 - 使用模型继承创建输入输出模型示例
# =============================================================================
# 本文件演示了如何使用 Pydantic 的模型继承来创建输入输出模型
#
# 【模型继承】
# Pydantic 模型支持继承，子模型会自动拥有父模型的所有字段。
# 这种方式可以：
# 1. 避免重复定义通用字段
# 2. 清晰地表达模型之间的关系
# 3. 便于维护和扩展
#
# 【使用场景】
# - 基础模型：包含所有模型共有的字段
# - 输入模型：在基础模型上添加输入特有的字段（如密码）
# - 输出模型：基础模型的子集（排除敏感字段）


# 导入 Pydantic
from pydantic import BaseModel, EmailStr  # Pydantic 基类和 EmailStr 类型

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义基础用户模型
class BaseUser(BaseModel):
    """
    基础用户模型

    包含所有用户模型共有的字段。
    这个模型定义了用户的基本信息。

    Attributes:
        username: 用户名
        email: 电子邮件地址
        full_name: 全名（可选）
    """
    username: str      # 必需：用户名
    email: EmailStr    # 必需：电子邮件地址（自动验证格式）
    full_name: str | None = None  # 可选：全名


# 定义用户输入模型（继承自 BaseUser）
class UserIn(BaseUser):
    """
    用户输入模型

    继承自 BaseUser，添加了密码字段。
    用于接收用户注册或更新信息。

    Attributes:
        password: 密码（继承自 BaseUser 的字段略）
    """
    password: str  # 必需：密码（父类中没有的字段）


# 定义创建用户的路由
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    """
    创建新用户

    使用模型继承来定义输入输出模型：
    - 输入：UserIn（继承自 BaseUser，包含密码）
    - 输出：BaseUser（不包含密码）

    Args:
        user: 用户信息，包含密码

    Returns:
        BaseUser: 用户基本信息，不包含密码

    Note:
        继承使得模型定义更加简洁，
        BaseUser 的字段自动包含在 UserIn 中。
    """
    return user


# 【模型继承的优势】
# 1. 代码复用：避免重复定义相同字段
# 2. 清晰的关系：明确表达模型间的层次结构
# 3. 易于维护：修改父模型自动影响所有子模型
# 4. 类型安全：获得完整的类型检查支持


# 【与其他方法的比较】
# 方法1：完全独立的模型
#   class UserIn(BaseModel):
#       username: str
#       email: EmailStr
#       full_name: str | None = None
#       password: str
#
#   class UserOut(BaseModel):
#       username: str
#       email: EmailStr
#       full_name: str | None = None
#   # 问题：重复定义相同字段

# 方法2：使用继承
#   class BaseUser(BaseModel):
#       username: str
#       email: EmailStr
#       full_name: str | None = None
#
#   class UserIn(BaseUser):
#       password: str
#
#   class UserOut(BaseUser):
#       pass
#   # 优势：代码复用，关系清晰


# 【实际应用场景】
# 1. 用户系统：
#    - BaseUser: 基础用户信息
#    - UserRegister: 注册（BaseUser + password）
#    - UserLogin: 登录（username + password）
#    - UserPublic: 公开信息（BaseUser）

# 2. 产品系统：
#    - BaseProduct: 基础产品信息
#    - ProductCreate: 创建产品（BaseProduct + 价格等）
#    - ProductUpdate: 更新产品（可选字段）
#    - ProductResponse: 响应（部分字段）

# 3. 订单系统：
#    - BaseOrder: 基础订单信息
#    - OrderCreate: 创建订单（BaseOrder + 详细物品）
#    - OrderResponse: 订单响应（简化版）


# 【测试方法】
# 1. 运行应用：uvicorn 07:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看继承关系的文档
