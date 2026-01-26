# 创建两个中间件，探索执行顺序
from fastapi import FastAPI 

# 创建 FastAPI 应用实例
app = FastAPI()

# 中间件1：在请求处理前打印请求路径
@app.middleware("http")
async def middleware1(request, call_next):
    print(f"[Middleware1] 收到请求：{request.url.path}")
    response = await call_next(request)
    print("[Middleware1] 响应已返回")
    return response

# 中间件2：在请求处理前打印请求方法
@app.middleware("http")
async def middleware2(request, call_next):
    print(f"[Middleware2] 请求方法：{request.method}")
    response = await call_next(request)
    print("[Middleware2] 响应结束")
    return response

@app.get("/items/{itemid}")
async def get_items(itemid:int):
  if itemid:
   return "hello"
  return "nihao"