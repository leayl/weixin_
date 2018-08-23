from urllib.parse import urlencode

import requests

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'IPLOC=CN5101; SUID=24FBD3DE5018910A000000005B398ABB; CXID=1630659C433618C020E6A6431EAA8A74; SUV=00C51783DED3FA8C5B4C349FD04DC306; ld=okllllllll2bnY$ElllllVH7dT6lllllTH5EJlllll9llllljklll5@@@@@@@@@@; ad=shH6Nlllll2byjHblllllVHheSylllllTH5fZZllll9lllllRPfils@@@@@@@@@@; ABTEST=0|1534757388|v1; SNUID=B6122A27F9FC8923760C5509FACCC28D; weixinIndexVisited=1; JSESSIONID=aaaqgEHX72X0O_ZRjGcvw; sct=10; ppinf=5|1534761361|1535970961|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OiVFNyVBRSU5Q3xjcnQ6MTA6MTUzNDc2MTM2MXxyZWZuaWNrOjk6JUU3JUFFJTlDfHVzZXJpZDo0NDpvOXQybHVESDA3bHJGMjIxZkpZQmp2UVFHejFvQHdlaXhpbi5zb2h1LmNvbXw; pprdig=RXGONFF04YUa3eVkTd4k6UwqEwGi0UBSwhoHT5y0jEar6AIPnKJVjm-B779WAeUD93CQy2-f2YvuUmcCEZzNjpGOsQS4lD1nv1XDoS7WJRWNtNrgQ6gZnNoCcXZQcDDvXinMkD7yMDF9QhzCImX2EkLDmdOwiWL0WsvXrkhP1Cc; sgid=09-36693223-AVt6mZGjzb9egS1RgY1pGKo; ppmdig=1534761362000000ba07bfba7bb30ccd443ee0a938350e53',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
proxy = None
proxy_pool_url='http://127.0.0.1:5000/get'
keyword = '朱一龙'

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url):
    global proxy
    try:
        if proxy:
            proxies = {
                'http':'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False )
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # ip被封后使用代理ip
            print(302)
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
    except ConnectionError:
        return get_html(url)

def get_index(keyword, page):
    data={
        'query':keyword,
        'type':2,
        'page':page,
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def main():
    for page in range(1,101):
        html = get_index(keyword, page)
        print(html)

if __name__ == '__main__':
    main()

