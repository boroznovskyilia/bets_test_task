"""add default to id

Revision ID: 520912c3c4a6
Revises: 95e18e1d082e
Create Date: 2024-11-06 10:52:25.018863

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "520912c3c4a6"
down_revision: Union[str, None] = "95e18e1d082e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("bet", sa.Column("created", sa.DateTime(), nullable=True))
    op.add_column("bet", sa.Column("updated", sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, "bet", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "bet", type_="unique")
    op.drop_column("bet", "updated")
    op.drop_column("bet", "created")
    # ### end Alembic commands ###