"""access_rights

Revision ID: 6c462154267e
Revises: 8377c94366c2
Create Date: 2026-08-07 18:18:05.849530

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c462154267e"
down_revision: Union[str, Sequence[str], None] = "8377c94366c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


roles = sa.table(
    "roles",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
    sa.column("is_active", sa.Boolean),
)

permisions = sa.table(
    "permisions",
    sa.column("id", sa.Integer),
    sa.column("resource", sa.String),
    sa.column("action", sa.String),
)

role_permisions = sa.table(
    "role_permisions",
    sa.column("role_id", sa.Integer),
    sa.column("permision_id", sa.Integer),
)


ROLE_NAMES = ("admin", "manager", "user")
PAGE_PERMISIONS = (
    ("common_page", "read"),
    ("manager_page", "read"),
    ("admin_page", "read"),
)

ROLE_ACCESS = {
    "admin": PAGE_PERMISIONS,
    "manager": (
        ("common_page", "read"),
        ("manager_page", "read"),
    ),
    "user": (("common_page", "read"),),
}


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        roles,
        [
            {"name": role_name, "is_active": True}
            for role_name in ROLE_NAMES
        ],
    )

    op.bulk_insert(
        permisions,
        [
            {"resource": resource, "action": action}
            for resource, action in PAGE_PERMISIONS
        ],
    )

    connection = op.get_bind()

    role_ids = dict(
        connection.execute(
            sa.select(roles.c.name, roles.c.id).where(
                roles.c.name.in_(ROLE_NAMES)
            )
        ).all()
    )
    permision_ids = {
        (resource, action): permision_id
        for resource, action, permision_id in connection.execute(
            sa.select(
                permisions.c.resource,
                permisions.c.action,
                permisions.c.id,
            ).where(
                sa.tuple_(permisions.c.resource, permisions.c.action).in_(
                    PAGE_PERMISIONS
                )
            )
        ).all()
    }

    op.bulk_insert(
        role_permisions,
        [
            {
                "role_id": role_ids[role_name],
                "permision_id": permision_ids[permision],
            }
            for role_name, role_access in ROLE_ACCESS.items()
            for permision in role_access
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()

    seeded_role_ids = sa.select(roles.c.id).where(
        roles.c.name.in_(ROLE_NAMES)
    )
    seeded_permision_ids = sa.select(permisions.c.id).where(
        sa.tuple_(permisions.c.resource, permisions.c.action).in_(
            PAGE_PERMISIONS
        )
    )

    connection.execute(
        role_permisions.delete().where(
            role_permisions.c.role_id.in_(seeded_role_ids),
            role_permisions.c.permision_id.in_(seeded_permision_ids),
        )
    )
    connection.execute(
        permisions.delete().where(permisions.c.id.in_(seeded_permision_ids))
    )
    connection.execute(roles.delete().where(roles.c.name.in_(ROLE_NAMES)))
