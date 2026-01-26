# =============================================================================
# FastAPI 入门 - 第一个 API 示例
# =============================================================================
# 本文件演示了如何创建一个最简单的 FastAPI 应用
#
# 【FastAPI 简介】
# FastAPI 是一个现代、快速（高性能）的 Python Web 框架，用于构建 API。
# 它基于 Python 3.6+ 的类型提示和 Pydantic，提供以下特性：
# 1. 高性能：基于 Starlette 和 Pydantic，速度可与 NodeJS 和 Go 媲美
# 2. 类型安全：利用 Python 类型提示进行数据验证
# 3. 自动文档：自动生成 OpenAPI 文档和 Swagger UI
# 4. 异步支持：原生支持 async/await 语法
#
# 【创建 FastAPI 应用】
# 创建 FastAPI 应用非常简单，只需实例化 FastAPI 类：
#   app = FastAPI()
#
# 【定义路径操作】
# FastAPI 使用装饰器来定义 API 端点（路径操作）：
#   @app.get("/")  # 处理 GET 请求到根路径 "/"
#   @app.post("/items/")  # 处理 POST 请求到 "/items/"
#   @app.put("/items/{item_id}")  # 处理 PUT 请求到 "/items/{item_id}"
#
# 【异步函数】
# 使用 async def 定义异步路径操作函数：
#   @app.get("/")
#   async def root():
#       return {"message": "Hello World"}
#
# 【返回值】
# FastAPI 会自动将返回值转换为 JSON 响应。
# 可以返回字典、列表、Pydantic 模型等，FastAPI 会自动处理序列化。
#
# 【运行应用】
# 使用 uvicorn 运行 FastAPI 应用：
#   uvicorn main:app --reload
# 其中：
#   - main: 是包含 FastAPI 应用的 Python 文件名
#   - app: 是 FastAPI 实例的名称
#   - --reload: 启用热重载，代码修改后自动重启服务
#
# 【访问 API 文档】
# 运行应用后，可以通过以下地址访问自动生成的 API 文档：
#   - Swagger UI: http://localhost:8000/docs
#   - ReDoc: http://localhost:8000/redoc
#   - OpenAPI JSON: http://localhost:8000/openapi.json


# 导入 FastAPI 类
# FastAPI 是框架的核心类，用于创建 API 应用实例
from fastapi import FastAPI

# 创建 FastAPI 应用实例
# 所有的 API 端点都将注册到这个 app 实例上
app = FastAPI()


# 定义 GET 请求的路径操作
# @app.get("/") 表示这个函数处理发送到根路径 "/" 的 GET 请求
# GET 请求用于从服务器获取数据
@app.get("/")
async def root():
    """
    根路径的 GET 请求处理函数

    Returns:
        dict: 返回一个包含欢迎消息的字典
    """
    # FastAPI 会自动将字典转换为 JSON 响应
    # 客户端收到的响应格式：{"message": "Hello World"}
    return {"message": "Hello World"}


# 【测试方法】
# 1. 确保安装了 FastAPI 和 uvicorn：
#    pip install fastapi uvicorn
#
# 2. 运行应用：
#    uvicorn 06:app --reload
#
# 3. 打开浏览器访问：http://localhost:8000
#    应该看到：{"message":"Hello World"}
#
# 4. 访问 API 文档：http://localhost:8000/docs
#    可以看到自动生成的 Swagger UI 文档
