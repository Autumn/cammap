from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base

class Submission(Base):
    __tablename__ = 'Submissions'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    lat = Column(Float)
    long = Column(Float)
    location = Column(String(140))
    comment = Column(String(140))

    def __init__(self, name=None, email=None):
        # TODO: Uhhhhhhh what
        self.date = None

    def __repr__(self):
        return '<Submission %d %f %f>' % (self.id, self.lat, self.long)
