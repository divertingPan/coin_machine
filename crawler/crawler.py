# -*- coding: utf-8 -*-

import requests, os.path, re, time, random
from bs4 import BeautifulSoup
import pandas as pd


requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s.keep_alive = False # 关闭多余连接

if not os.path.isdir('./standard_img'):
    os.makedirs('./standard_img')

# reference: https://blog.csdn.net/jamesaonier/article/details/89003053
agentPools = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50"
    ]
headers = {'User-Agent': random.choice(agentPools)}


"""
要设置ip代理，不然封ip之后很难受，但是这些都是免费proxy，不太稳，要做好措施
reference: https://blog.csdn.net/weixin_37719937/article/details/99060349
           https://github.com/jhao104/proxy_pool
           
嫌麻烦也可以使用商业软件，每日可以白嫖10个ip，但是都是国内proxy
           http://www.zhiyoudaili.com/getapi.html
实测用国内ip访问ucoin都慢，容易断线，最好还是直接挂科学上网
"""
with open('./ip.txt', 'r') as f:
    ip_pool = f.readlines()

def get_proxy():
    # r = random.choice(ip_pool).strip('\n')
    # r = requests.get("http://120.79.85.144/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=1&fa=0&groupid=0&fetch_key=&qty=1&time=1&port=1&format=txt&ss=1&css=&pro=&city=&dt=1&usertype=6").text
    # r = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
    # proxy = {'https': r}
    proxy = ''
    return proxy

# 测试ip有没有成功改变
# res = requests.get('https://www.ipip.net/', proxies=get_proxy(), headers=headers).text


if __name__ == '__main__':

    # reference: https://www.jianshu.com/p/2b783f7914c6

    # # 第一级 - 获取所有国家地区的列表
    # index_url = 'https://zh-cn.ucoin.net/catalog'
    # res = requests.get(index_url, proxies=get_proxy(), headers=headers)  # 不加header会被拦截
    # soup = BeautifulSoup(res.text, 'html.parser')
    # # print(res.text)
    
    # country_list = soup.find_all('li', class_='cntry')
    # country_link_list = []
    # country_name_list = []
    # for tag in country_list:
    #     country_link = 'https://zh-cn.ucoin.net' + tag.a['href']
    #     country_link_list.append(country_link)
        
    #     country_name = tag.a.find('span', class_='left wrap nopad').get_text()
    #     country_name_list.append(country_name)
    # print('total counrty: ', len(country_name_list))
    
    # data = {'country_name':country_name_list, 'country_link':country_link_list}
    # dataframe = pd.DataFrame(data)
    # dataframe.to_csv(r'./country_link_list.csv', index=False, encoding='utf-8_sig')
        
    
    # # 第二级 - 获取一个国家的所有时代和币种
    # if os.path.exists('./country_link_list.csv'):
    #     df = pd.read_csv('./country_link_list.csv')
    #     country_link_list = [x for x in df['country_link']]
    
    # all_class_list = []
    # for i, index_url in enumerate(country_link_list):
    # # index_url = country_link_list[390]
    #     print(i, '/', len(country_name_list), 'searching: ', index_url)

    #     res = requests.get(index_url, proxies=get_proxy(), headers=headers)  # 不加header会被拦截
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     time.sleep(3)
        
    #     class_list = soup.find_all('ul', class_='left hor-switcher')
    #     if len(class_list) == 0:
    #         raise RuntimeError('IP banned!')
    
    #     for all_tag in class_list:
    #         period_tag = all_tag.find_all('a', class_='switcher')
            
    #         for class_tag in period_tag:
    #             class_tag = 'https://zh-cn.ucoin.net/catalog/' + class_tag['href']
    #             all_class_list.append(class_tag)
    # print(len(all_class_list))
    
    # data = {'all_class_list':all_class_list}
    # dataframe = pd.DataFrame(data)
    # dataframe.to_csv(r'./all_class_list.csv', index=False, encoding='utf-8_sig')


    # 第三级 - 获取当前页面的所有硬币
    
    if os.path.exists('./all_class_list.csv'):
        df = pd.read_csv('./all_class_list.csv')
        all_class_list = [x for x in df['all_class_list']]    
        
    if os.path.exists('./coin_name_link_list.csv'):
        df = pd.read_csv('./coin_name_link_list.csv')
        beginning = [x for x in df['flag']]
        if not beginning == []:
            beginning = beginning[-1] + 1  # 万一中途还是坏了，可以从半截开始
        else:
            beginning = 0
    else:
        data = {'coin_name':[], 'link':[], 'flag': 0}
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(r'./coin_name_link_list.csv', mode='a', index=False, encoding='utf-8_sig')
        beginning = 0
    
    for i, index_url in enumerate(all_class_list[beginning:], start=beginning):
    # index_url = all_class_list[0]
        coin_link_list = []
        coin_name_list = []
        
        print(i, '/', len(all_class_list), 'searching')
        print(index_url)
        
        res = requests.get(index_url, proxies=get_proxy(), headers=headers)  # 不加header会被拦截
        # res = requests.get(index_url, headers=headers)  # 不加header会被拦截
        soup = BeautifulSoup(res.text, 'html.parser')
        time.sleep(3)
        
        coin_link = soup.find_all('a', class_='value')
        if len(coin_link) == 0:
            raise RuntimeError('IP banned!')
        
        for i_coin, tag in enumerate(coin_link):
            tag = 'https://zh-cn.ucoin.net' + tag['href']
            res = requests.get(tag, proxies=get_proxy(), headers=headers)  # 不加header会被拦截
            # res = requests.get(tag, headers=headers)  # 不加header会被拦截
            soup = BeautifulSoup(res.text, 'html.parser')
            time.sleep(3)
            
            img_td = soup.find_all('td', class_='i')
            if len(img_td) == 0:
                raise RuntimeError('IP banned!')
    
            for img in img_td:
                print(i_coin, '/', len(coin_link), img.img['alt'])
                if img.img['alt'] == 'No Image':
                    break
                    
                img = img.a['href']
                
                # 每抓完一个页面的图才存一次表格
                filename = ''.join(re.findall(r'.*https://i.ucoin.net/coin/(.*)', img))
                filename = filename.replace("/", "_");
                coin_name_list.append(filename)
                coin_link_list.append(tag)
                
                print('saving image: ', filename)
                with open('./standard_img/' + filename, 'wb') as f:
                    f.write(requests.get(img, proxies=get_proxy(), headers=headers).content)  # 时刻记住要加header
                    # f.write(requests.get(img, headers=headers).content)  # 时刻记住要加header
                time.sleep(3)
        
        data = {'coin_name':coin_name_list, 'link':coin_link_list, 'flag': i}
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(r'./coin_name_link_list.csv', mode='a', header=False, index=False, encoding='utf-8_sig')
        print('********** list updated **********')