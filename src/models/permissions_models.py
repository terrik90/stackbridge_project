from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import BaseModel, TimestampMixin, intpk

if TYPE_CHECKING:
    from src.models.users_models import RolesModel


class PermisionsModel(BaseModel, TimestampMixin):
    __tablename__ = "permisions"

    id: Mapped[intpk]
    resource: Mapped[str] = mapped_column(String(256), nullable=False)
    action: Mapped[str] = mapped_column(String(256), nullable=False)

    role: Mapped[list["RolesModel"]] = relationship(
        back_populates="permisions", secondary="role_permisions"
    )

    __table_args__ = (
        UniqueConstraint(
            "resource",
            "action",
            name="uq_permisions_resource_action",
        ),
    )


class RolePermisionsModel(BaseModel, TimestampMixin):
    __tablename__ = "role_permisions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permision_id: Mapped[int] = mapped_column(
        ForeignKey("permisions.id"), primary_key=True
    )
