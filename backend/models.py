from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base

class Submission(Base):
    __tablename__ = 'Submissions'
    # TODO: We aren't using sqlite for much longer
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    lat = Column(Float)
    long = Column(Float)
    radius = Column(Integer)
    location = Column(String(140))
    comment = Column(String(140))

    def __init__(self, name=None, email=None):
        # TODO: Uhhhhhhh what
        self.date = None

    def __repr__(self):
        return '<Submission %d %f %f>' % (self.id, self.lat, self.long)
