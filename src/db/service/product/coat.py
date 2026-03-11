from db.config.engine import EngineDB
from sqlalchemy import text
from pathlib import Path
import pandas as pd
from datetime import datetime

class CoatService:

    def __init__(self, user: str = None, password: str = None):
        self.session = EngineDB().get_engine()
        
    async def insert_data(self, data: dict | list) -> None:
        async with self.session as s:
            await s.execute(
                    text("""
                        INSERT INTO product.coat (id, supplier_id, name, description, brand_id, price_basic, price_product, images, characteristics, sizes, total_quantity, rating, feedbacks_count) 
                        VALUES (:id, :seller_id, :name, :description, :brand_id, :price_basic, :price_product, :images, :characteristics, :sizes, :total_quantity, :rating, :feedbacks_count)
                        ON CONFLICT (id) DO NOTHING
                    """),
                    data
            )
            await s.commit()

    async def clear_table(self):
        async with self.session as s:
            await s.execute(
                text("TRUNCATE TABLE product.coat;")
            )
            await s.commit()

    async def generate_excel(self, ru: bool = False):
        sql_file = 'db/sql/execl_ru.sql' if ru else 'db/sql/execl.sql'
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_query = f.read()
            async with self.session as s:
                result = await s.execute(text(sql_query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                """
                Сохраняет DataFrame в Excel с красивым форматированием
                """
                filename = '../excel/coat_ru.xlsx' if ru else '../excel/coat.xlsx'
                
                # Создаем Excel файл с форматированием
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='coat', index=False)
                    
                    # Получаем рабочий лист для форматирования
                    worksheet = writer.sheets['coat']
                    
                    # Автоматическая ширина колонок
                    for column in df:
                        column_width = max(df[column].astype(str).map(len).max(), len(column))
                        col_idx = df.columns.get_loc(column)
                        worksheet.column_dimensions[chr(65 + col_idx)].width = min(column_width + 2, 50)