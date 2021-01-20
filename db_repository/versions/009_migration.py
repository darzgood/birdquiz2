from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz = Table('quiz', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
    Column('timestamp', DATETIME),
    Column('images', TEXT),
    Column('questionTotal', INTEGER),
    Column('questionComplete', INTEGER),
    Column('questionCorrect', FLOAT),
    Column('setupComplete', INTEGER),
    Column('photos', BLOB),
    Column('currentBird', VARCHAR(length=60)),
    Column('retry', INTEGER),
    Column('allPhotosDict', BLOB),
    Column('availablePhotosDict', BLOB),
    Column('currentImage', VARCHAR(length=60)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz'].columns['currentBird'].drop()
    pre_meta.tables['quiz'].columns['images'].drop()
    pre_meta.tables['quiz'].columns['photos'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz'].columns['currentBird'].create()
    pre_meta.tables['quiz'].columns['images'].create()
    pre_meta.tables['quiz'].columns['photos'].create()
