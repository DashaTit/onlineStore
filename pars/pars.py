import requests
import json
from data_requests import Data_requests



def get_data():
    data_req= Data_requests(0)
    cookies = data_req.cookies
    headers = data_req.headers
    params = data_req.params
    response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies, headers=headers).json()
    products_id = response['body']['products']
    with open('id_products.json', 'w') as file:
        json.dump(products_id, file, indent=4, ensure_ascii=False)
    json_data = {
        'productIds': products_id,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
        'multioffer': False,
}

    response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers, json=json_data).json()

    with open('2_items.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    products_id_str = ','.join(products_id)

    params = {
        'productIds': products_id_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies, headers=headers).json()

    with open('prices.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    items_prices = {}

    material_prices = response['body']['materialPrices']

    for item in material_prices:
        item_id = item['price']['productId']
        item_base_price = item['price']['basePrice']

        items_prices[item_id] = {
            'item_basePrice': item_base_price,
        }

    with open('final_prices.json', 'w', encoding='utf-8') as file:
        json.dump(items_prices, file, indent=4, ensure_ascii=False)



def get_result():
    with open('2_items.json', encoding='utf-8') as file:
        products_data = json.load(file)

    with open('final_prices.json', encoding='utf-8') as file:
        products_prices = json.load(file)

    products_data = products_data['body']['products']

    for item in products_data:
        products_id = item['productId']

        if products_id in products_prices:
            prices = products_prices[products_id]
        
        item['item_basePrice'] = prices['item_basePrice']

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

get_data()
get_result()