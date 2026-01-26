from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

sqlite_file_name = "data_new.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 使用 WAL 模式和超时设置来解决锁定问题
engine = create_engine(
    sqlite_url, 
    echo=True,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # 设置30秒超时
    },
    poolclass=None,  # 禁用连接池
)

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import text

def create_db_and_tables():
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))  # 启用 WAL 模式
        conn.commit()

def create_user():
    with engine.begin() as conn:  # 使用 begin() 而不是 connect()
        stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")
        result = conn.execute(stmt)
        print(f"Created user with id: {result.inserted_primary_key}")

def query_users():
    with engine.connect() as conn:
        stmt = select(User)
        results = conn.execute(stmt)
        users = results.all()
        print("Users in database:")
        for user in users:
            print(user)

def query_uesr1():
    with engine.connect() as conn:
        stmt = select(User).where(User.name == "spongebob")
        results = conn.execute(stmt)
        user = results.first()
        print(user)

if __name__ == "__main__":
  create_db_and_tables()
  create_user()
  query_uesr1()


 
  
