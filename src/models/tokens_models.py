from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import ActiveMixin, BaseModel, TimestampMixin, intpk

if TYPE_CHECKING:
    from src.models.users_models import UsersModel


class TokensModel(BaseModel, TimestampMixin, ActiveMixin):
    __tablename__ = "tokens"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    user: Mapped["UsersModel"] = relationship(back_populates="tokens")
