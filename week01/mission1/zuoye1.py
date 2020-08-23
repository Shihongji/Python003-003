# requests bs4 爬取猫眼 top10，＋名称、上映时间，进去爬取类型；
# 以 UTF-8 保存 csv——pandas

import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd


# bs4是第三方库需要使用pip命令安装
def get_in_movie(mov10):
    tp10 = []
    for url in mov10:
        print(url)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

        header = {'user-agent': user_agent}

        response_in = requests.get(url, headers=header)
        print(response_in.status_code)

        b_soup = bs(response_in.text, 'html.parser')

        # 名称
        movie_name = b_soup.find('h1', attrs={'class': 'name'}).text
        # 类型
        movie_class = b_soup.find_all('a', attrs={'class': 'text-link'})
        movie_cates = ''
        for cate in movie_class:
            movie_cates += cate.text

        # 时间
        movie_release_date = b_soup.find_all('li', attrs={'class': 'ellipsis'})[2].text[:10]

        tp = [movie_name, movie_cates, movie_release_date]
        tp10.append(tp)

    return tp10

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

header = {'user-agent':user_agent}

myurl = 'https://maoyan.com/board/4'

response = requests.get(myurl, headers=header)

bs_info = bs(response.text, 'html.parser')

movie_list = []

# Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
for tags in bs_info.find_all('div', attrs={'class': 'movie-item-info'}):
    for atag in tags.find_all('a'):
        short_href = atag.get('href')
        ab_href = 'https://maoyan.com'+ short_href
        movie_list.append(ab_href)
        # 获取所有链接
        sleep(1)
print(movie_list)

movie_ans = get_in_movie(movie_list)

movie_data = pd.DataFrame(data=movie_ans)
movie_data.to_csv('./maoyan10.csv', encoding='utf-8', index=False, header=False)



