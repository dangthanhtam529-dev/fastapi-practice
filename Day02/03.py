# =============================================================================
# FastAPI 路径参数 - 枚举类型路径参数示例
# =============================================================================
# 本文件演示了如何使用 Python 枚举（Enum）作为路径参数的类型
#
# 【为什么要使用枚举类型？】
# 当路径参数只能取特定的值时，使用枚举类型可以：
# 1. 限制输入：只允许预定义的值
# 2. 提供文档：自动生成的 API 文档会显示所有可能的值
# 3. 类型安全：在代码中进行类型检查
# 4. IDE 支持：编辑器提供代码补全
#
# 【Python 枚举（Enum）】
# Python 的 enum 模块提供了 Enum 类来创建枚举：
#   from enum import Enum
#
#   class ModelName(str, Enum):
#       alexnet = "alexnet"
#       resnet = "resnet"
#       lenet = "lenet"
#
# 这里 ModelName 继承自 str 和 Enum：
# - 继承 str：枚举值是字符串类型，可以与字符串比较
# - 继承 Enum：可以使用枚举的所有功能
#
# 【枚举的特点】
# 1. 枚举成员有名称和值：
#    ModelName.alexnet.name   # "alexnet"
#    ModelName.alexnet.value  # "alexnet"
#
# 2. 可以使用 "is" 或 "==" 比较枚举成员：
#    model_name is ModelName.alexnet
#    model_name == ModelName.alexnet
#
# 3. 可以通过值获取枚举成员：
#    ModelName("alexnet")  # 返回 ModelName.alexnet
#
# 【FastAPI 中的枚举路径参数】
# 定义路径参数类型为枚举类：
#   @app.get("/models/{model_name}")
#   async def get_model(model_name: ModelName):
#
# FastAPI 会：
# 1. 验证路径参数是否在枚举定义的值中
# 2. 如果不在，返回 422 错误
# 3. 如果在，将参数转换为枚举成员


# 导入所需的模块
from enum import Enum  # Python 标准库的枚举模块

from fastapi import FastAPI  # FastAPI 框架


# 定义枚举类，用于限制路径参数的可选值
# 继承 str 和 Enum，使枚举值同时具有字符串和枚举的特性
class ModelName(str, Enum):
    """
    机器学习模型名称枚举

    继承 str 使得枚举值可以直接作为字符串使用
    继承 Enum 提供枚举的所有功能

    Members:
        alexnet: AlexNet 模型
        resnet: ResNet 模型
        lenet: LeNet 模型
    """
    alexnet = "alexnet"  # 枚举成员的值是字符串 "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# 创建 FastAPI 应用实例
app = FastAPI()


# 定义路径操作，路径参数使用枚举类型
# 访问 /models/alexnet、/models/resnet、/models/lenet 会匹配这个路由
# 访问其他值会返回 422 错误
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    获取指定模型的信息

    Args:
        model_name: 模型名称，必须是 ModelName 枚举的成员之一

    Returns:
        dict: 包含模型名称和对应消息的字典

    Raises:
        HTTPException: 如果 model_name 不是有效的枚举值，返回 422 错误
    """
    # 使用 "is" 比较枚举成员（推荐使用 "is" 或 "is not"）
    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }

    # 也可以使用 .value 比较字符串值
    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }

    # 默认情况（resnet）
    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }


# 【测试方法】
# 1. 运行应用：uvicorn 03:app --reload
# 2. 访问 http://localhost:8000/models/alexnet
#    返回：{"model_name":"alexnet","message":"Deep Learning FTW!"}
# 3. 访问 http://localhost:8000/models/resnet
#    返回：{"model_name":"resnet","message":"Have some residuals"}
# 4. 访问 http://localhost:8000/models/vgg
#    返回：422 错误（"vgg" 不是有效的枚举值）
# 5. 访问 http://localhost:8000/docs 查看 API 文档


# 【枚举路径参数的实际应用场景】
# - 状态查询：/orders/{status}，status 只能是 pending/paid/shipped
# - 版本选择：/api/{version}，version 只能是 v1/v2/v3
# - 模式切换：/model/{mode}，mode 只能是 train/predict/evaluate
# - 类型过滤：/products/{category}，category 只能是预定义的商品类别
