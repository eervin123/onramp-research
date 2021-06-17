from typing import List

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
    def get_all_history(symbol: String, session: Session) -> List["CloseData"]:
        stmt = text("SELECT * FROM close_data where symbol=:symbol")
        return session.query(CloseData).from_statement(stmt)\
            .params(symbol=symbol).all()

    @staticmethod
    def get_multiple_histories(symbols: List[str], session: Session) -> List["CloseData"]:
        symbol_joins = ",".join(symbols)
        stmt = text("SELECT * FROM close_data where symbol in (:symbol_joins)")
        return session.query(CloseData).from_statement(stmt)\
            .params(symbol_joins=symbol_joins).all()
