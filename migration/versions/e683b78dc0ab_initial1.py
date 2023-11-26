"""initial1

Revision ID: e683b78dc0ab
Revises: 008a35300e38
Create Date: 2023-11-17 19:18:28.299054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e683b78dc0ab'
down_revision: Union[str, None] = '008a35300e38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pupil', sa.Column('school_name', sa.Boolean(), nullable=False))
    op.drop_column('pupil', 'notify')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pupil', sa.Column('notify', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('pupil', 'school_name')
    # ### end Alembic commands ###
