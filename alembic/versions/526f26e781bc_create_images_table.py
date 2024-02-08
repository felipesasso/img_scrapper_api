"""create images table

Revision ID: 526f26e781bc
Revises: 
Create Date: 2024-02-07 14:27:03.771675

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "526f26e781bc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "images",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("image", sa.BLOB, nullable=False),
    )


def downgrade():
    op.drop_table("images")
