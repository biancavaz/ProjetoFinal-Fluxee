"""tabela disciplina criada

Revision ID: 1fea1aa53f7f
Revises: a8dbf1f422ad
Create Date: 2025-11-27 22:44:34.363321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fea1aa53f7f'
down_revision = 'a8dbf1f422ad'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('solicitacao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('disciplina_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_solicitacao_disciplina',   # NOME CORRETO DA FK
            'disciplina',
            ['disciplina_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('solicitacao', schema=None) as batch_op:
        batch_op.drop_constraint('fk_solicitacao_disciplina', type_='foreignkey')
        batch_op.drop_column('disciplina_id')
