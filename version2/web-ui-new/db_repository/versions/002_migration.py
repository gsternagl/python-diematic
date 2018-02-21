from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('user_id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=20)),
    Column('email', VARCHAR(length=30), nullable=False),
    Column('password', VARCHAR, nullable=False),
    Column('registered_on', DATETIME),
)

users = Table('users', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('login', String(length=20)),
    Column('email', String(length=30), nullable=False),
    Column('password', String, nullable=False),
    Column('registered_on', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['username'].drop()
    post_meta.tables['users'].columns['login'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['username'].create()
    post_meta.tables['users'].columns['login'].drop()
