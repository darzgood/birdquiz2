from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz_vars = Table('quiz_vars', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('questionTotal', Integer),
    Column('questionComplete', Integer),
    Column('questionCorrect', Integer),
    Column('images', Text),
    Column('user_id', Integer),
)

score = Table('score', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('quiz_id', Integer),
    Column('score', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['quiz_vars'].create()
    post_meta.tables['score'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['quiz_vars'].drop()
    post_meta.tables['score'].drop()
