from sqlalchemy import Column, Integer, String, Float, DateTime, desc
from backend.database import Base

class Submission(Base):
    __tablename__ = 'Submissions'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    lat = Column(Float)
    long = Column(Float)
    radius = Column(Integer)
    location = Column(String(140))
    comment = Column(String(140))

    def __init__(self, myid, date, lat, long, radius, location, comment):
        # TODO: Uhhhhhhh what
        self.id = myid
        self.date = date
        self.lat = lat
        self.long = long
        self.radius = radius
        self.location = location
        self.comment = comment

    def __repr__(self):
        return '<Submission %d %f %f>' % (self.id, self.lat, self.long)

