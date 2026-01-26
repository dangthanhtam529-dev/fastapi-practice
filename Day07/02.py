from fastapi import FastAPI
from sqlmodel.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase ,mapped_column, relationship,Mapped

app = FastAPI()

# 异步数据库引擎
ASYNC_DATA_URL = "mysql+aiomysql://root:@localhost:3306/fastapi_test?charset=utf8mb4"
async_engine = create_async_engine(ASYNC_DATA_URL, 
  echo=True,
  pool_pre_ping=True,
  max_overflow=10,
)

# 基类
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(default_factory=datetime.now)
    update_time: Mapped[datetime] = mapped_column(default_factory=datetime.now, onupdate=datetime.now)


