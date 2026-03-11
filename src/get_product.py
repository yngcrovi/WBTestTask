from extract_data import extract_product_info
import requests

# Заголовки для запросов 
HEADERS = {
    # Базовые
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    
    # Дополнительные
    "accept":"*/*",
    "accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie":"_wbauid=1462901791773161254; x_wbaas_token=1.1000.b3e4a4a72e544c6e918830152ec5c4dd.MHwzNy4xNTMuNTUuMTI3fE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDUuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzc0MzcwOTcwfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3Mzc2NjE3MHwx.MEUCICAAeb7LQc5+rVMIwjBTTooEs4YSEmcGo2qvcprp6dbjAiEAotFBzxWs3/1tYV7BT3BVDBXCy3aMbZQH4AqGw7pcY8w=",
    "deviceid":"site_2ed9822adcd74d1aa4815fd260f30076",
    "priority":"u=1, i",
    "referer":"https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8",
    "sec-ch-ua":'"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":'"Windows"',
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "x-queryid":"qid146290179177316125420260310183503",
    "x-requested-with":"XMLHttpRequest",
    "x-spa-version":"14.0.7",
    "x-userid":"0"
}

def get_product(ru: bool = False) -> list:

    product_list: list[dict] = []
    # Берём 50 страниц
    for page in range(1, 51):

        # url для получения товаров по запросу "пальто из натуральной шерсти"
        url = f'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_online_redirect_dc=unreg_dm&ab_retrieval=seara_05&appType=1&curr=rub&dest=123589415&hide_vflags=4294967296&lang=ru&page={page}&query=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE+%D0%B8%D0%B7+%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9+%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false'
        
        # GET-параметр для фильтра по стране производителя - Россия
        ru_param = {
            'f14177451': '15000203'
        }

        # Отправляем GET-запрос с заголовками
        response = requests.get(url, headers=HEADERS, params=(ru_param if ru else {}))

        data = response.json()

        for product in data['products']:
            product_list.append(extract_product_info(product))

    return product_list