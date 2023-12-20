import requests as r
from bs4 import BeautifulSoup as bs
from dict_elements import page_products
import math
import re
import json


def max_page(url,headers):
    req=r.get(url,headers)
    soup = bs(req.content, 'html.parser').select_one("span[class='product-facet__meta-bar-item product-facet__meta-bar-item--count']").text
    product_amount = int(''.join(filter(str.isdigit, soup)))
    max_page = math.ceil(product_amount / page_products)
    return max_page,product_amount

def items_info(url,headers):
    req = r.get(url, headers).text
    soup = bs(req, 'lxml')
    scripts = soup.findAll('script')
    for s in scripts:
        if 'var meta' in s.text:
            script = s.text
            script = script.split('var meta = ')[1]
            script = script.split(';\nfor (var attr in meta)')[0]
            jsonStr = script
            jsonObj = json.loads(jsonStr)
    return jsonObj

def item_parse(url,headers):
    req = r.get(url+'.json', headers).text
    try:
        req_json=json.loads(req)
    except json.decoder.JSONDecodeError as e:
        return
    data='General:'+req_json['product']['tags']
    key_value_pairs = [item.strip() for item in data.split(',')]

    # Initialize an empty dictionary
    data_dict = {}

    # Populate the dictionary with key-value pairs
    for pair in key_value_pairs:
        key_value = map(str.strip, pair.split(':', 1))
        key, *values = key_value
        # If the key already exists, convert the existing value to a list
        if key in data_dict:
            existing_value = data_dict[key]
            if not isinstance(existing_value, list):
                existing_value = [existing_value]
            data_dict[key] = existing_value + values
        else:
            data_dict[key] = values[0] if values else None

    try:
        category=data_dict['Category']
        category = [category] if not isinstance(category, list) else category
    except:
        category=''

    try:
        composition=data_dict['Composition']
    except:
        composition=''

    result_list = []

    for variant in req_json['product']['variants']:
        result = [
            {"key": "productName", "value": req_json['product']['title'], "type": "text"},
            {"key": "description", "value": req_json['product']['body_html'], "type": "text"},
            {"key": "price", "value": variant['price'], "type": "text"},
            {"key": "brandId", "value": req_json['product']['vendor'], "type": "text"},
            {"key": "categoryId", "value": category[0] if len(category) !=0 else '', "type": "text"},
            {"key": "subCategoryId", "value": category[1] if len(category) >1 else '', "type": "text"},
            {"key": "innerCategoryId", "value": category[2] if len(category) >2 else '', "type": "text"},
            {"key": "productTypeId", "value": variant['sku'], "type": "text"},
            {"key": "composition", "value": composition, "type": "text"},
            {"key": "product_ID", "value": str(req_json['product']['id']), "type": "text"},
            {"key": "highlights", "value": "", "type": "text"},
            {"key": "wearing", "value": "", "type": "text"},  # You can fill this with relevant data
            {"key": "washingInstruction", "value": "", "type": "text"},  # You can fill this with relevant data
            {"key": "isSizeAvailable", "value": "1", "type": "text"},
            {"key": "quantity", "value": str(variant['quantity_rule']['min']), "type": "text"},
            {"key": "sizeId", "value": "", "type": "text", "disabled": True},
            {"key": "onSizePrice", "value": "", "type": "text", "disabled": True}
        ]
        result_list.append(result)

    return result_list


def remove_patterns(input_string):
    patterns = [r'\s*-\s*XS',r'\s*-\s*S',r'\s*-\s*M', r'\s*-\s*O/S', r'\s*-\s*3XL',r'\s*-\s*L',r'\s*-\s*XL',r'\s*-\s*L',r'\s*-\s*XXL']
    for pattern in patterns:
        output_string = re.sub(pattern, '', input_string)
    return output_string