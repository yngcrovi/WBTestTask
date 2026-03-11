import json

def extract_product_info(data: dict[str, dict | list[dict[str, dict]] | int | str]) -> dict:
    """
    Извлекает информацию о товаре с Wildberries из словаря
    """
    result = {}
    article = data.get('id')
    # Артикул
    result['id'] = article
    
    # Название
    result['name'] = data.get('name')
    
    # Цена 
    if data.get('sizes') and len(data['sizes']) > 0:
        price_info = data['sizes'][0].get('price', {})
        # Цена в копейках, переводим в рубли
        basic_price = price_info.get('basic', 0) / 100
        product_price = price_info.get('product', 0) / 100
        result['price_basic'] = basic_price  # Базовая цена
        result['price_product'] = product_price  # Цена со скидкой
    else:
        result['price_basic'] = None
        result['price_product'] = None
    
    # Описание
    result['description'] = f"{data.get('name', '')} от бренда {data.get('brand', '')}"
    
    # Ссылки на изображения через запятую
    pics_count = data.get('pics', 0)
    if pics_count > 0 and article:
        # Стандартный формат ссылок на изображения Wildberries
        images = []
        for i in range(1, pics_count + 1):
            # Для первых 10 изображений используется один шаблон, для остальных - другой
            if i <= 10:
                img_url = f"https://basket-{str(article)[0]}.wb.ru/vol{article//100000}/part{article//1000}/{article}/images/big/{i}.jpg"
            else:
                img_url = f"https://basket-{str(article)[0]}.wb.ru/vol{article//100000}/part{article//1000}/{article}/images/big/{i}.jpg"
            images.append(img_url)
        result['images'] = images
    else:
        result['images'] = None
    
    # Все характеристики
    # Копируем все данные, но удаляем некоторые поля для чистоты
    characteristics = data.copy()
    # Удаляем поля, которые уже извлекли отдельно или которые не нужны в характеристиках
    exclude_keys = ['id', 'name', 'brand', 'supplier', 'rating', 'feedbacks', 
                    'sizes', 'pics', 'totalQuantity', 'meta', 'logs']
    for key in exclude_keys:
        characteristics.pop(key, None)
    
    # Добавляем информацию о цветах из colors
    if data.get('colors'):
        characteristics['colors'] = [color.get('name') for color in data['colors'] if color.get('name')]
    
    result['characteristics'] = json.dumps(characteristics, ensure_ascii=False)
    
    # Название селлера
    result['seller_name'] = data.get('supplier') or data.get('brand')
    
    # Ссылка на селлера
    result['seller_id'] = data.get('supplierId')
    
    # Размеры товара через запятую
    if data.get('sizes'):
        result['sizes'] = [size.get('name') for size in data['sizes'] if size.get('name')]
    else:
        result['sizes'] = []
    
    # Остатки по товару (общее количество)
    result['total_quantity'] = data.get('totalQuantity')
    
    # Рейтинг
    result['rating'] = data.get('reviewRating') or data.get('rating')
    
    # Количество отзывов
    result['feedbacks_count'] = data.get('feedbacks') or data.get('nmFeedbacks')
    
    # Бренд
    result["brand_id"] = data.get('brandId', None)
    result["brand_name"] = data.get('brand', None)

    return result