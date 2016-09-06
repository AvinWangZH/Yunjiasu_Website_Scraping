from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pickle
import re
import csv



def get_link(start_url):
    standard_url = 'http://www.15yunmall.com'
    
    data = urlopen(start_url)
    bsObj = BeautifulSoup(data.read())
    
    link = list(bsObj.find_all('a', {'class': 'member-info member-bottom'}))
    link.append(bsObj.find('a', {'class': 'member-info '}))
    
    if link == [None]:
        link = list(bsObj.find_all('a', {'class': 'thumbnail href href-goods'}))
        
    link_list = []
    
    if link != [None]:
        for i in link:
            link_list.append(standard_url + i['href'])
        
    return link_list    

def get_good_info(page_url):
    
    #data are: ‘品名’，'购买价格'， ‘推广赠送’， ‘库存量’， ‘已售出’， ‘商品详情’， ‘客服电话’ 
    
    data = urlopen(page_url)
    bsObj = BeautifulSoup(data.read())
    
    good_info = {}
    good_list = []
    good_dict = {}
    
    #find ‘品名’
    name_html = bsObj.find_all('p', {'class': 'prodetail-title'})
    try: 
        name = (name_html[0].text).replace('品名：', '')  
    except IndexError:
        name = ''
    
    good_info['品名'] = name
    good_list.append(name)
    good_dict[name] = {}
    
    #find '购买价格'
    price_info = bsObj.find_all('p', {'class': 'prodetail-score'})
    try: 
        price = price_info[0].text.replace('购买价格：', '')
    except IndexError:
        price = ''
    good_info['购买价格'] = price
    good_list.append(price)
    good_dict[name]['购买价格'] = price
    
    #find '购买价格'
    try:
        promotion = price_info[1].text.replace('推广赠送：', '')
    except IndexError:
        promotion = ''
    good_info['推广赠送'] = promotion
    good_list.append(promotion)
    good_dict[name]['推广赠送'] = promotion
    
    #find 库存量
    stock_info = bsObj.find_all('span', {'id': 'prodetail-stock'})
    try: 
        stock = stock_info[0].text.replace('库存量：', '')
    except IndexError:
        stock = ''
    good_info['库存量'] = stock
    good_list.append(stock)
    good_dict[name]['库存量'] = stock
    
    #find 已售出
    sale_info = bsObj.find_all(text = re.compile('已售出'))
    try: 
        sale = sale_info[0].replace('已售出：', '')   
    except IndexError:
        sale = ''
    good_info['已售出'] = sale
    good_list.append(sale)
    good_dict[name]['已售出'] = sale
    
    #find 商品详情
    provider_info = bsObj.find_all('span', {'style': 'color: #009943;font-weight: 200;'})
    try:
        provider = provider_info[0].text.replace('商品详情：', '').replace('\xa0', '')
    except IndexError:
        provider = ''
    good_info['商品详情（公司）'] = provider
    good_list.append(provider)
    good_dict[name]['商品详情（公司）'] = provider
    
    #find 客服电话
    phone_info = bsObj.find_all(text = re.compile('客服电话'))
    if phone_info != []:
        phone = phone_info[0].replace('客服电话 \xa0->', '').strip()
    else:
        phone = ''
    good_info['客服电话'] = phone
    good_list.append(phone)
    good_dict[name]['客服电话'] = phone
    
    return good_list, good_dict #good_info, good_list

def get_all_goods_info():
    with open('all_good_link_yunjiasu.json', 'r') as f:
        link_list = json.load(f) 
        
    all_goods = []
    all_goods_dict = {}
    
    count = 0
    
    for i in link_list:
        good_list, good_dict = get_good_info(i)
        all_goods.append(good_list)
        all_goods_dict.update(good_dict)
        count += 1
        if count == 50:
            break
        print(count)
    
    with open('all_goods_list_yunjiasu.json', 'w') as f:
        json.dump(all_goods, f)
        
    with open('all_goods_dict_yunjiasu.json', 'w') as f:
        json.dump(all_goods_dict, f)    
        
    return all_goods_dict
        
    
if __name__ == '__main__':
    pass
