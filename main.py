from bs4 import BeautifulSoup
import re
if __name__ == '__main__':
    soup = BeautifulSoup(open("scrape_center/test.html",encoding="utf-8"), 'lxml')
    published_time = soup.find(text=(re.compile(r'上映'))).string.split()[0]
    print(type(published_time))



