from sqlalchemy import Column, String, Float, Date, text
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import Session

Base = declarative_base()

class CloseData(Base):
    __tablename__ = 'close_data'

    symbol = Column(String, primary_key=True)
    close = Column(Float)
    date = Column(Date, primary_key=True)

    @staticmethod
    def get_all_history(symbol: String, session: Session):
        stmt = text("SELECT * FROM close_data where symbol=:symbol")
        return session.query(CloseData).from_statement(stmt)\
            .params(symbol=symbol).all()
