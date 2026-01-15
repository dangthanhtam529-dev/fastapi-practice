# 带路径的路径参数
from fastapi import FastAPI

app = FastAPI()

# 虽然fastapi并不会直接推荐使用带路径的路径参数，
# 但是在某些情况下，例如文件上传下载等场景，使用带路径的路径参数是非常方便的
# 路径参数可以包含路径，例如 /files/home/johndoe/myfile.txt，
# 可以使用 {file_path:path} 来匹配所有路径
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}