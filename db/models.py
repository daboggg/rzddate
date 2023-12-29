from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


# class User(Base):
#     __tablename__ = "user_account"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))

class TaskTable(Base):
    __tablename__ = "task_table"

    id: Mapped[str] = mapped_column(primary_key=True)
    trigg_name: Mapped[str]
    chat_id: Mapped[int]
    run_date: Mapped[str]
    date_of_trip: Mapped[str]
    text: Mapped[str]