import os

from sqlalchemy import create_engine

class DbToCsvTransformer:
    def __init__(self):
        self.engine = create_engine(os.getenv("sqlalchemy.url"))

    def load_asset_data_from_db(self):
        self.engine.