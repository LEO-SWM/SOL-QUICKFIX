from sqlalchemy import Column, String
from models import Base


class Order(Base):
    __tablename__ = "orders"

    Seriennummer = Column(String(50), primary_key=True)
    Auftragsnummer = Column(String(50), default="unknown")
    Datum = Column(String(50), default="unknown")
    Materialnummer = Column(String(50), default="unknown")
    Liefermenge = Column(String(50), default="unknown")
    Mengeneinheit = Column(String(50), default="unknown")
    Anschrift1 = Column(String(50), default="unknown")
    Anschrift2 = Column(String(50), default="unknown")
    Anschrift3 = Column(String(50), default="unknown")
