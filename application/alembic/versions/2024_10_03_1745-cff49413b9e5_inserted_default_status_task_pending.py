"""Inserted default status task = PENDING

Revision ID: cff49413b9e5
Revises: 3d7eea21e14b
Create Date: 2024-10-03 17:45:39.317286

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cff49413b9e5"
down_revision: Union[str, None] = "3d7eea21e14b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
