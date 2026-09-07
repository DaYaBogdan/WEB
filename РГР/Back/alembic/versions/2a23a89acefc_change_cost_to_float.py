"""change cost to float

Revision ID: 2a23a89acefc
Revises: b9748db1d6f3
Create Date: 2026-09-07 19:10:15.340320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a23a89acefc'
down_revision: Union[str, Sequence[str], None] = 'b9748db1d6f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('tasks', 'cost',
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )

def downgrade():
    op.alter_column('tasks', 'cost',
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
