from typing import List

from sqlalchemy import Column, String, Float, DateTime, text
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class CryptocurrencyPairOHLCV(Base):
    __tablename__ = 'cryptocurrency_pairs'

    asset_1 = Column(String, primary_key=True)
    asset_2 = Column(String, primary_key=True)
    price_close = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_open = Column(Float)
    volume = Column(Float)
    datetime = Column(DateTime, primary_key=True)

    @staticmethod
    def get_all_history_for_pair(asset_1: String, asset_2: String, session: Session) -> List["CryptocurrencyPairOHLCV"]:
        stmt = text("SELECT * FROM cryptocurrency_pairs where asset_1=:asset_1 and asset_2=:asset_2")
        return session.query(CryptocurrencyPairOHLCV).from_statement(stmt) \
            .params(asset_1=asset_1, asset_2=asset_2).all()
