from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz = Table('quiz', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('timestamp', DateTime),
    Column('images', Text),
    Column('questionTotal', Integer),
    Column('questionComplete', Integer),
    Column('questionCorrect', Float),
    Column('setupComplete', Integer),
    Column('photos', PickleType),
    Column('currentBird', String(length=60)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['quiz'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['quiz'].drop()
