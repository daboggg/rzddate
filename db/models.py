from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task_table"

    id: Mapped[str] = mapped_column(primary_key=True)
    trigg_name: Mapped[str]
    chat_id: Mapped[int]
    run_date: Mapped[str]
    date_of_trip: Mapped[str]
    text: Mapped[str]