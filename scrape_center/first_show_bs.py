from first_show import *
from bs4 import BeautifulSoup
import bs4


def parse_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    img = soup.find(name='img', class_="cover").attrs['src'].strip()
    name = soup.find(name='h2', class_="m-b-sm").string.strip()
    categories_div = soup.find(name="div", class_="categories")
    categories = [child.span.string.strip() for child in categories_div.contents if isinstance(child, bs4.element.Tag)]
    published_time = soup.find(text=(re.compile(r'上映'))).string.split(" ")[0] if soup.find(
        text=(re.compile(r'上映'))) else None
    drama = soup.find(name="div", class_="drama").p.string.strip()
    score = soup.find(name="p", class_="score").string.strip()
    ret = {
        "img": img,
        "name": name,
        "category": categories,
        "published_time": published_time,
        "drama": drama,
        "score": float(score)
    }
    return ret


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
