# =============================================================================
# FastAPI 路径参数 - 包含斜杠的路径参数示例
# =============================================================================
# 本文件演示了如何使用可以包含斜杠（/）的路径参数
#
# 【普通路径参数的局限性】
# 普通路径参数默认不能包含斜杠（/）：
#   @app.get("/files/{file_path}")
#   async def read_file(file_path: str):
#
# 这个路由只能匹配：
#   - /files/abc
#   - /files/123
#
# 但不能匹配包含路径的文件：
#   - /files/home/johndoe/myfile.txt
#   - /files/folder/subfolder/document.pdf
#
# 【带路径的路径参数】
# 使用 ":path" 后缀可以匹配包含斜杠的路径：
#   @app.get("/files/{file_path:path}")
#   async def read_file(file_path: str):
#
# 这个路由可以匹配：
#   - /files/home/johndoe/myfile.txt
#   - /files/folder/subfolder/document.pdf
#   - /files/（空路径）
#
# 【使用场景】
# 1. 文件服务：/files/{file_path:path} 用于文件下载
# 2. 静态资源：/static/{path:path} 用于静态文件服务
# 3. 代理转发：/proxy/{path:path} 用于代理其他服务
# 4. CDN 资源：/cdn/{resource_path:path} 用于 CDN 资源管理
#
# 【注意事项】
# 1. 带路径的参数会匹配尽可能长的路径
# 2. 如果有其他路由可以匹配，应该将更具体的路由放在前面
# 3. 需要对路径进行安全检查，防止路径遍历攻击


# 导入 FastAPI
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义带路径的路径参数路由
# ":path" 后缀告诉 FastAPI 这个参数可以包含斜杠
# 可以匹配 /files/ 后面的任意路径，包括包含子路径的情况
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    读取文件路径

    Args:
        file_path: 文件路径，可以包含斜杠

    Returns:
        dict: 包含文件路径的字典

    Examples:
        - /files/document.txt -> {"file_path": "document.txt"}
        - /files/home/user/file.txt -> {"file_path": "home/user/file.txt"}
        - /files/folder/subfolder/file.pdf -> {"file_path": "folder/subfolder/file.pdf"}
    """
    return {"file_path": file_path}


# 【测试方法】
# 1. 运行应用：uvicorn 04:app --reload
# 2. 访问 http://localhost:8000/files/document.txt
#    返回：{"file_path":"document.txt"}
# 3. 访问 http://localhost:8000/files/home/johndoe/myfile.txt
#    返回：{"file_path":"home/johndoe/myfile.txt"}
# 4. 访问 http://localhost:8000/files/folder/subfolder/file.pdf
#    返回：{"file_path":"folder/subfolder/file.pdf"}


# 【实际应用示例】
# 结合文件服务的完整示例：
#
#   @app.get("/files/{file_path:path}")
#   async def download_file(file_path: str):
#       # 确保文件路径安全，防止路径遍历攻击
#       safe_path = Path(file_path).resolve()
#       base_path = Path("/safe/directory")
#
#       if not safe_path.is_relative_to(base_path):
#           raise HTTPException(status_code=403, detail="Forbidden")
#
#       # 返回文件内容
#       return FileResponse(safe_path)
#
# 【注意事项】
# 1. 生产环境中需要对路径进行安全检查
# 2. 防止用户访问不应该访问的文件（路径遍历攻击）
# 3. 考虑使用 base_path 限制可访问的目录范围
# 4. 对于敏感文件，不要暴露直接的路径访问接口
