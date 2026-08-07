from datetime import datetime
from typing import Annotated

from sqlalchemy import Boolean, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

intpk = Annotated[
    int,
    mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    ),
]


class BaseModel(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class ActiveMixin:
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
