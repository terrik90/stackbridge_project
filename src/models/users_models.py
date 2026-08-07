from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import ActiveMixin, BaseModel, TimestampMixin, intpk

if TYPE_CHECKING:
    from src.models.permissions_models import PermisionsModel
    from src.models.tokens_models import TokensModel


class RolesModel(BaseModel, ActiveMixin):
    __tablename__ = "roles"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)

    users: Mapped[list["UsersModel"]] = relationship(back_populates="role")

    permisions: Mapped[list["PermisionsModel"]] = relationship(
        back_populates="role", secondary="role_permisions"
    )


class UsersModel(BaseModel, TimestampMixin, ActiveMixin):
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

    role: Mapped["RolesModel"] = relationship(back_populates="users")

    tokens: Mapped[list["TokensModel"]] = relationship(back_populates="user")
