import requests, random 
from lxml import html

min_compl_len = 30 
max_compl_len = 200 

def get_compliments():
    """Функции скрабинга комплиментов со страницы сайта с комплиментами"""
    complCollection = []
    for i in range(2,7):
        page = requests.get('https://datki.net/komplimenti/zhenshine/page/{page_number}/')
        tree = html.fromstring(page.content)  
        complCollection.extend(tree.xpath('//a[@class="post-copy btn"]/@data-clipboard-text'))
    
    compliments = []
    for compliment in complCollection:  
            if (len(compliment) >= min_compl_len) and (len(compliment) < max_compl_len): 
                compliments.append(compliment) 

    return random.choice(compliments)

