from db.service.brand import BrandService
from db.service.supplier import SupplierService
from db.service.product.coat import CoatService
from get_product import get_product


async def insert_brand(data: dict):
    await BrandService().insert_data(data)

async def insert_supplier(data: dict):
    await SupplierService().insert_data(data)

async def generate_excel_product(data: dict, ru: bool = False):
    await CoatService().insert_data(data)
    await CoatService().generate_excel(ru=(True if ru else False))

async def clear_table():
    await CoatService().clear_table()


if __name__ == '__main__':
    import asyncio
    product_list = get_product()
    asyncio.run(insert_brand(product_list))
    asyncio.run(insert_supplier(product_list))
    asyncio.run(generate_excel_product(product_list))
    asyncio.run(clear_table())
    product_list = get_product(True)
    asyncio.run(generate_excel_product(product_list, True))