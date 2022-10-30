import requests
import logging
from insert_data import *


LIMIT=10
TOTAL_PAGE =10
category_list = ['name','alias','cover','categories','score','published_at','drama']
INDEX_URL = "https://spa1.scrape.center/api/movie?limit={limit}&offset={offset}"
DETAIL_URL = "https://spa1.scrape.center/api/movie/{idx}"
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',)


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT,offset=max(0,LIMIT*(page-1)))
    return scrape_api(url)

def scrape_api(url):
    logging.info(f"scrape {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error(f"get invalid status_code {response.status_code} while scraping {url}")
    except requests.RequestException:
        logging.error(f"error occurred while scraping {url}")
def scrape_detail(idx):
    url = DETAIL_URL.format(idx=idx)
    return scrape_api(url)

def main():
    datamanager = DataManager(host= host,user=user,password=password,db='spiders') # 连接数据库
    for page in range(TOTAL_PAGE):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            idx = item.get("id")
            detail_data = scrape_detail(idx)
            use_detail_data = {key:str(detail_data.get(key)) if detail_data.get(key) else None for key in category_list}
            # 将解析后的数据存入数据库中
            datamanager.save_data(use_detail_data)
            logging.info("detail data %s",use_detail_data)


if __name__ == '__main__':
    main()
