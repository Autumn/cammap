from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base

class Submission(Base):
    __tablename__ = 'Submissions'
    # TODO: We aren't using sqlite for much longer
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    lati = Column(Float)
    longi = Column(Float)
    radius = Column(Integer)
    location = Column(String(140))
    comment = Column(String(140))

    def __init__(self, myid, date, lati, longi, radius, location, comment):
        # TODO: Uhhhhhhh what
        self.id = myid
        self.date = date
        self.lati = lati
        self.longi = longi
        self.radius = radius
        self.location = location
        self.comment = comment

    def __repr__(self):
        return '<Submission %d %f %f>' % (self.id, self.lati, self.longi)
