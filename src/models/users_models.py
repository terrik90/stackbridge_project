from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import ActiveMixin, Base_model, TimestampMixin, intpk

if TYPE_CHECKING:
    from src.models.permissions_models import Permisions_model
    from src.models.tokens_models import Tokens_model


class Roles_model(Base_model, ActiveMixin):
    __tablename__ = "roles"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)

    users: Mapped[list["Users_model"]] = relationship(back_populates="role")

    permisions: Mapped[list["Permisions_model"]] = relationship(
        back_populates="role", secondary="role_permisions"
    )


class Users_model(Base_model, TimestampMixin, ActiveMixin):
    __tablename__ = "users"

    id: Mapped[intpk]
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id"), nullable=False
    )

    role: Mapped["Roles_model"] = relationship(back_populates="users")

    tokens: Mapped[list["Tokens_model"]] = relationship(back_populates="user")
