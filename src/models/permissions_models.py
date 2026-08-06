from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import Base_model, TimestampMixin, intpk

if TYPE_CHECKING:
    from src.models.users_models import Roles_model


class Permisions_model(Base_model, TimestampMixin):
    __tablename__ = "permisions"

    id: Mapped[intpk]
    resource: Mapped[str] = mapped_column(String(256), nullable=False)
    action: Mapped[str] = mapped_column(String(256), nullable=False)

    role: Mapped[list["Roles_model"]] = relationship(
        back_populates="permisions", secondary="role_permisions"
    )


class Role_permisions_model(Base_model, TimestampMixin):
    __tablename__ = "role_permisions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permision_id: Mapped[int] = mapped_column(
        ForeignKey("permisions.id"), primary_key=True
    )
