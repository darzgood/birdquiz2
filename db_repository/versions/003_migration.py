from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz_vars = Table('quiz_vars', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('questionTotal', INTEGER),
    Column('questionComplete', INTEGER),
    Column('questionCorrect', INTEGER),
    Column('images', TEXT),
    Column('user_id', INTEGER),
)

score = Table('score', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
    Column('quiz_id', INTEGER),
    Column('score', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
)

quiz = Table('quiz', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('timestamp', DateTime),
    Column('images', Text),
    Column('questionTotal', Integer),
    Column('questionComplete', Integer),
    Column('questionCorrect', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz_vars'].drop()
    pre_meta.tables['score'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['quiz'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz_vars'].create()
    pre_meta.tables['score'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['quiz'].drop()
