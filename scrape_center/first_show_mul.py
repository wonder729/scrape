from first_show import *

import multiprocessing


def main(page):
    detail_list = []
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for one_detail_url in detail_urls:
        detail_html = scrape_detail(one_detail_url)
        detail = parse_detail(detail_html)
        detail_list.append(detail)
        logging.info(f"get deatil {detail}")
    return detail_list

def run(main_fun):
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    data = pool.map(main_fun, pages)
    pool.close()
    pool.join()
    save_data(data, "mul_movies.xlsx")
    logging.info(f"save successful")


if __name__ == '__main__':
    run(main)
