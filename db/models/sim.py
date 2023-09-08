from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base


class Sim(Base):
    __tablename__ = 'sims'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship("User", backref=backref("sims", cascade="all, delete"))
