"""Add enrollment_number and password_changed to users table

Revision ID: add_auth_fields
Revises: e20b79799835
Create Date: 2024-03-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_auth_fields'
down_revision = 'e20b79799835'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('student', 'admin', name='roleenum'), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('enrollment_number', sa.String(), nullable=True),
        sa.Column('password_changed', sa.Boolean(), server_default='false', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('enrollment_number', name='uq_users_enrollment_number'),
    )
    op.create_index('ix_users_username', 'users', ['username'])


def downgrade() -> None:
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')