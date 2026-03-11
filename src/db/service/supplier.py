from db.config.engine import EngineDB
from sqlalchemy import text

class SupplierService:

    def __init__(self, user: str = None, password: str = None):
        self.session = EngineDB().get_engine()
        
    async def insert_data(self, data: dict | list) -> None:
        async with self.session as s:
            await s.execute(
                    text("""
                        INSERT INTO supplier (id, name) 
                        VALUES (:seller_id, :seller_name)
                        ON CONFLICT (id) DO NOTHING
                    """),
                    data
            )
            await s.commit()