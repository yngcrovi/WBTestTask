from db.config.engine import EngineDB
from sqlalchemy import text

class BrandService:

    def __init__(self, user: str = None, password: str = None):
        self.session = EngineDB().get_engine()
        
    async def insert_data(self, data: dict | list) -> None:
        async with self.session as s:
            await s.execute(
                    text("""
                        INSERT INTO brand (id, name) 
                        VALUES (:brand_id, :brand_name)
                        ON CONFLICT (id) DO NOTHING
                    """),
                    data
            )
            await s.commit()