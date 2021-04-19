#!/usr/bin/python3
import cgitb; cgitb.enable()
import json
import requests

error_log = ""
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
bottlo_prices = {}
bottlo_urls = {
    'Liquor Land':{
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
    },
    'First Choice':{
        'corona':{
            'url':'https://www.firstchoiceliquor.com.au/api/products/fc/qld/beer/54492', 
            'referer':'https://www.firstchoiceliquor.com.au/',
            'cookies':''
        },    
        'summer':{
            'url':'https://www.firstchoiceliquor.com.au/api/products/ll/qld/beer/2124456',
            'referer':'https://www.firstchoiceliquor.com.au/',
            'cookies':''
        }    
    },
    'BWS':{
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
    },
    'Dan Murphys':{
        'corona':{
            'url':'https://api.danmurphys.com.au/apis/ui/Product/357480',
            'referer':'https://api.danmurphys.com.au/',
            'cookies':''
        },    
        'summer':{
            'url':'https://api.danmurphys.com.au/apis/ui/Product/797597',
            'referer':'https://api.danmurphys.com.au/',
            'cookies':''
        }    
    }
}
for shop in bottlo_urls:
    bottlo_prices[shop] = {}
    for beer in bottlo_urls[shop]:
        headers = {
            'User-Agent': user_agent,
            'Referer': bottlo_urls[shop][beer]['referer'],
            'Cookie': bottlo_urls[shop][beer]['cookies'] 
        }
        response = requests.get(bottlo_urls[shop][beer]['url'], headers=headers)
        try:
            data = response.json()
            if shop == 'BWS':    
                # Iterate through data to find price of case
                for item in data['Products']:
                   for info in item['AdditionalDetails']:
                        if(info['Name'] == "webpacktype" and info['Value'] == "Case"):
                           # Get price of case and append to bws_prices
                           bottlo_prices[shop].update({beer : "%.2f"%item['Price']})
            elif shop == 'Dan Murphys':  
                bottlo_prices[shop].update({beer : "%.2f" % data['Products'][0]['Prices']['caseprice']['Value']})
            else :
                bottlo_prices[shop].update({beer : "%.2f" % data['product']['price']['current']})
        except ValueError as e:
            str(bottlo_urls[shop][beer])+" Unexpected Response /n "+response.text+" /n".join(error_log)
            # del bottlo_prices[shop]
json_dump = json.dumps(bottlo_prices)
print ("Content-type: application/json\n")
print (json_dump)
