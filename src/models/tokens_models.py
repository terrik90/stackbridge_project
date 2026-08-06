from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import ActiveMixin, Base_model, TimestampMixin, intpk

if TYPE_CHECKING:
    from src.models.users_models import Users_model


class Tokens_model(Base_model, TimestampMixin, ActiveMixin):
    __tablename__ = "tokens"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    user: Mapped["Users_model"] = relationship(back_populates="tokens")
