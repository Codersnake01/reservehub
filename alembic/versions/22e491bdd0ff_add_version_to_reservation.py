"""add_version_to_reservation

Revision ID: 22e491bdd0ff
Revises: 981008c5c55d
Create Date: 2026-07-31 15:08:25.507930

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "22e491bdd0ff"
down_revision: Union[str, None] = "981008c5c55d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Añadir columna version con valor por defecto para filas existentes
    op.add_column(
        "reservations", sa.Column("version", sa.Integer(), server_default="1")
    )
    op.execute("UPDATE reservations SET version = 1")
    op.alter_column("reservations", "version", nullable=False)


def downgrade() -> None:
    op.drop_column("reservations", "version")
