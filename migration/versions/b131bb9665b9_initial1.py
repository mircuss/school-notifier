"""initial1

Revision ID: b131bb9665b9
Revises: 5df18898b593
Create Date: 2023-11-26 16:10:53.971606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b131bb9665b9'
down_revision: Union[str, None] = '5df18898b593'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pupil', 'school_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pupil', sa.Column('school_name', sa.BOOLEAN(), nullable=False))
    # ### end Alembic commands ###