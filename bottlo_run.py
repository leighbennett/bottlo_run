#!/usr/bin/python3
import cgitb; cgitb.enable()
import json
import requests

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

def get_first_choice_prices():
    # Dictionary of URLs to webscrape from
    first_choice_urls = {
        'corona':'https://www.firstchoiceliquor.com.au/api/products/fc/qld/beer/54492', 
        'summer':'https://www.firstchoiceliquor.com.au/api/products/ll/qld/beer/2124456'
    }
    # Empty Dictionary to store prices
    first_choice_prices = {}
    # Iterate through bws_urls
    for beer in first_choice_urls:
        # Fake Request Headers
        headers = {'User-Agent': user_agent, 'Referer': first_choice_urls[beer]}
        # Connect to the URL
        response = requests.get(first_choice_urls[beer], headers=headers)
        # Parse Json response
        data = response.json()
        # Get price of case and append to bws_prices 
        first_choice_prices[beer] = "%.2f" % data['product']['price']['current']
    # Return dictionary of prices                
    return first_choice_prices

def get_liquor_land_prices():
    # Dictionary of URLs to webscrape from
    liqour_land_urls = { 
         'corona':{
            'url' :'https://www.liquorland.com.au/api/products/ll/qld/beer/54492', 
            'referer' :'https://www.firstchoiceliquor.com.au/beer/corona-bottle-355ml_54492',
            'cookies' :'__uzma=5c46ed6a-63d6-411c-a080-f6ee191added;__uzmb=1608678083;__uzmc=806744049432;__uzmd=1608678208;'
         },
         'summer':{
            'url':'https://www.liquorland.com.au/api/products/ll/qld/beer/2124456',
            'referer':'https://www.firstchoiceliquor.com.au/beer/summer-bright-lime-bottle-330ml_2124456',
            'cookies':'__uzma=5c46ed6a-63d6-411c-a080-f6ee191added;__uzmb=1608678083;__uzmc=806744049432;__uzmd=1608678208;'
         }   
    }
    # Empty Dictionary to store prices
    liqour_land_prices = {}
    # Iterate through bws_urls
    for beer in liqour_land_urls:
        # Fake Request Headers
        headers = {'User-Agent': user_agent, 'Referer': liqour_land_urls[beer]['referer'],'Cookie': liqour_land_urls[beer]['cookies'] }
        # Connect to the URL
        response = requests.get(liqour_land_urls[beer]['url'], headers=headers)
        # Parse Json response
        data = response.json()
        # Get price of case and append to bws_prices 
        liqour_land_prices[beer] = "%.2f" % data['product']['price']['current']
    # Return dictionary of prices                
    return liqour_land_prices

def get_bws_prices():
    # Dictionary of URLs to webscrape from
    bws_urls = {
        'corona':{
            'url':'https://api.bws.com.au/apis/ui/Product/357480',
            'referer':'https://bws.com.au/product/357480/corona-extra-beer-bottles-355ml',
            'cookies':'w-lrkswrdjp=dm-Delivery,f-2125,s-0;'
        },    
        'summer':{
            'url':'https://api.bws.com.au/apis/ui/Product/797597',
            'referer':'https://bws.com.au/product/797597/xxxx-summer-bright-lager-with-natural-lime',
            'cookies':'w-lrkswrdjp=dm-Delivery,f-2125,s-0;'
        }    
    }
    # Empty Dictionary to store prices
    bws_prices = {}
    # Iterate through bws_urls
    for beer in bws_urls: 
        # Fake Request Headers
        headers = {'User-Agent': user_agent, 'Referer': bws_urls[beer]['referer'],'Cookie': bws_urls[beer]['cookies'] }
        # Connect to the URL
        response = requests.get(bws_urls[beer]['url'], headers=headers)
        # Parse Json response
        data = response.json()
        # Iterate through data to find price of case
        for item in data['Products']:
           for info in item['AdditionalDetails']:
                if(info['Name'] == "webpacktype" and info['Value'] == "Case"):
                   # Get price of case and append to bws_prices
                   bws_prices[beer] = "%.2f"%item['Price'] 
    # Return dictionary of prices                
    return bws_prices

def get_dan_murphys_prices():
    # Dictionary of URLs to webscrape from
    dan_murphys_urls = {
        'corona':'https://api.danmurphys.com.au/apis/ui/Product/357480',
        'summer':'https://api.danmurphys.com.au/apis/ui/Product/797597'
    }
    # Empty Dictionary to store prices
    dan_murphys_prices = {}
    # Iterate through dan_murphys_urls
    for beer in dan_murphys_urls: 
        # Connect to the URL
        response = requests.get(dan_murphys_urls[beer])
        # Parse Json response
        data = response.json()
        # Get price of case and append to dan_murphys_prices 
        dan_murphys_prices[beer] = "%.2f" % data['Products'][0]['Prices']['caseprice']['Value']
    # Return dictionary of prices    
    return dan_murphys_prices

bottlo = {} 
bottlo['Dan Murphys'] = get_dan_murphys_prices()
bottlo['BWS'] = get_bws_prices()
#bottlo['Liquor Land'] = get_liquor_land_prices()
bottlo['first choice'] = get_first_choice_prices()
json_dump = json.dumps(bottlo)
print ("Content-type: application/json\n")
print (json_dump)
