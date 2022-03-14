"""Added racetrack_api tables

Revision ID: 9234e34c6309
Revises: 
Create Date: 2022-03-05 21:26:42.686571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9234e34c6309'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('races',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('place', sa.String(length=256), nullable=True),
    sa.Column('race_date', sa.Date(), nullable=True),
    sa.Column('race_time', sa.Time(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_complete', sa.Boolean(), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['users.id'], name='fk_races_users_id_owner'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('races', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_races_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_races_race_date'), ['race_date'], unique=False)

    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('race', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['race'], ['races.id'], name='fk_cars_races_id_race'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('race', 'number', name='uc_cars_race_number')
    )
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cars_number'), ['number'], unique=False)

    op.create_table('heats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('race', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('ran_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['race'], ['races.id'], name='fk_heats_races_id_race'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('race', 'number', name='uc_heats_race_number')
    )
    with op.batch_alter_table('heats', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_heats_number'), ['number'], unique=False)

    op.create_table('lanes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('race', sa.Integer(), nullable=True),
    sa.Column('color', sa.String(length=16), nullable=True),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['race'], ['races.id'], name='fk_lanes_races_id_race'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('race', 'number', name='uc_lanes_race_number')
    )
    with op.batch_alter_table('lanes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_lanes_number'), ['number'], unique=False)

    op.create_table('runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('mph', sa.Float(), nullable=False),
    sa.Column('fps', sa.Float(), nullable=False),
    sa.Column('mps', sa.Float(), nullable=False),
    sa.Column('race', sa.Integer(), nullable=True),
    sa.Column('heat', sa.Integer(), nullable=True),
    sa.Column('lane', sa.Integer(), nullable=True),
    sa.Column('car', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car'], ['cars.id'], name='fk_runs_cars_id_car'),
    sa.ForeignKeyConstraint(['heat'], ['heats.id'], name='fk_runs_heats_id_heat'),
    sa.ForeignKeyConstraint(['lane'], ['lanes.id'], name='fk_runs_lanes_id_lane'),
    sa.ForeignKeyConstraint(['race'], ['races.id'], name='fk_runs_races_id_race'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('heat', 'car', name='uc_runs_heat_car'),
    sa.UniqueConstraint('heat', 'lane', name='uc_runs_heat_lane')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('runs')
    with op.batch_alter_table('lanes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lanes_number'))

    op.drop_table('lanes')
    with op.batch_alter_table('heats', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_heats_number'))

    op.drop_table('heats')
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cars_number'))

    op.drop_table('cars')
    with op.batch_alter_table('races', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_races_race_date'))
        batch_op.drop_index(batch_op.f('ix_races_name'))

    op.drop_table('races')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))

    op.drop_table('users')
    # ### end Alembic commands ###
