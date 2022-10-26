import requests
import re
import logging
from urllib.parse import urljoin
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s', )
#                     filename='spider.log',filemode='a'

BASE_URL = "https://ssr1.scrape.center"
TOTAL_PAGE = 10


def scrape_page(url):
    logging.info(f"scrape {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.info(f"get invalid status_code {response.status_code} while scraping {url}")
    except requests.RequestException:
        logging.info(f"error occurred while scraping {url}")


def scrape_index(page):
    index_url = f"{BASE_URL}/page/{page}"
    return scrape_page(index_url)


def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)

    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info(f"get detail url {detail_url}")
        yield detail_url


def scrape_detail(url):
    return scrape_page(url)


def parse_detail(html):
    img_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)  # page_link
    name_pattern = re.compile('<h2.*?class="m-b-sm">(.*?)</h2>.*?class="categories">', re.S)  # str
    category_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>', re.S)  # list
    published_time_pattern = re.compile('<span.*?>(\d{4}-\d{2}-\d{2}) 上映</span>', re.S)  # str
    drama_pattern = re.compile('<div.*?drama.*?<p.*?>(.*?)</p>', re.S)  # str
    score_pattern = re.compile('<div.*?class="score.*?(\d\.\d)</p>', re.S)  # float

    img = re.search(img_pattern, html).group(1).strip() if re.search(img_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    category = re.findall(category_pattern, html) if re.findall(category_pattern, html) else []
    published_time = re.search(published_time_pattern, html).group(1).strip() if re.search(published_time_pattern,
                                                                                           html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = re.search(score_pattern, html).group(1).strip() if re.search(score_pattern, html) else None

    ret = {
        "img": img,
        "name": name,
        "category": category,
        "published_time": published_time,
        "drama": drama,
        "score": float(score)
    }
    return ret


def save_data(data_list, name='movies.xlsx'):
    if any(isinstance(i, list) for i in data_list):
        data = []
        for i in data_list:
            data.extend(i)
        data_list = data
    data_df = pd.DataFrame(data_list)
    data_df.to_excel(name, index=False)


def main():
    data = []
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        for one_detail_url in detail_urls:
            one_detail_html = scrape_detail(one_detail_url)
            detail = parse_detail(one_detail_html)
            data.append(detail)
            logging.info(f"get deatil {detail}")
    save_data(data)
    logging.info("save movies.xlsx")


if __name__ == '__main__':
    main()