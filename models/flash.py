from sqlalchemy import Column, String
from models import Base


class Flash(Base):
    __tablename__ = "flash"

    Seriennummer = Column(String(50), primary_key=True)
    PMAX = Column(String(50), default="unknown")
    ISC = Column(String(50), default="unknown")
    VOC = Column(String(50), default="unknown")
    IPM = Column(String(50), default="unknown")
    VPM = Column(String(50), default="unknown")
    Paletten = Column(String(50), default="unknown")
    Container = Column(String(50), default="unknown")
