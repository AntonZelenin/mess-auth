from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.models import Base


class MyModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    # user_id: Mapped[int] = mapped_column(primary_key=True)
