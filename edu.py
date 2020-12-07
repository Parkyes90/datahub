import csv
import os
from requests_html import HTMLSession

import requests
from bs4 import BeautifulSoup
import multiprocessing
from selenium import webdriver
import parse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from common import BASE_DIR, write_csv, DATA_DIR, CATEGORY, options


def get_url(ntt_id, bbs_id):
    return (
        f"http://happyedu.moe.go.kr"
        f"/happy/bbs/selectHappyArticle.do"
        f"?nttId={ntt_id}"
        f"&bbsId={bbs_id}"
    )


def get_list_by_page(driver):
    ret = []
    titles = driver.find_elements_by_css_selector(".search_lister")
    for title in titles:
        date = title.find_element_by_class_name("date")
        span = title.find_element_by_class_name("title").get_attribute(
            "onclick"
        )
        if "img" in span:
            parsed = parse.parse(
                "fn_happy_articlList_img('{ntt_id}', '{bbs_id}')", span
            )
        elif "report" in span:
            parsed = parse.parse(
                "fn_happy_report('{ntt_id}', '{bbs_id}')", span
            )
        else:
            parsed = parse.parse(
                "fn_happy_article('{ntt_id}', '{bbs_id}')", span
            )

        ret.append(
            {
                "date": date.text.split("-")[0],
                "link": get_url(
                    parsed.named["ntt_id"], parsed.named["bbs_id"]
                ),
            }
        )
    return ret


def get_all_list():
    driver = webdriver.Chrome(os.path.join(BASE_DIR, "chromedriver"))

    links = []
    url = (
        "http://happyedu.moe.go.kr"
        "/happy/happyESSearch.do"
        "?detailsFlag=normal"
        "&mainKeyword=미래+교육"
        "&detailsKeyword1="
        "&detailsKeyword2="
        "&upperMenuNo="
        "&sort="
        "&range="
        "&dateFlag="
        "&dateS="
        "&dateE="
        "&pageIndex=1"
        "&searchCnd="
    )
    driver.get(url)
    cats = driver.find_elements_by_class_name("lister_foot_btn")
    cat = cats[0]
    more = cat.find_element_by_tag_name("a")
    more.click()

    for i in range(1, 7):
        tabs = driver.find_elements_by_css_selector(".search_tab a")
        tabs[i].click()
        links += get_list_by_page(driver)
        next_page = 2
        while True:
            try:
                next_button = driver.find_element_by_css_selector(
                    f"[href='?pageIndex={next_page}']"
                )
                links += get_list_by_page(driver)
                next_page += 1
                next_button.click()
            except NoSuchElementException:
                break
    driver.close()
    return links


def get_links():
    ret = set()
    with open(os.path.join(DATA_DIR, "output", "edu_detail_links.csv")) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            ret.add((row[0], row[1]))
            # year, link = row
    ret = list(ret)
    ret.sort()
    index_list = []
    for idx, r in enumerate(ret):
        index_list.append([*r, idx])
    return index_list


def get_detail(item):
    year, link, idx = item
    print(idx)
    driver = webdriver.Chrome(
        os.path.join(BASE_DIR, "chromedriver"), options=options
    )
    driver.get(link)
    context = driver.find_element_by_tag_name("body").text
    title = driver.title
    driver.close()
    return {
        "category": CATEGORY,
        "year": year,
        "title": title,
        "context": context,
    }


if __name__ == "__main__":
    # link = get_all_list()
    # write_csv(link, "output", "edu_detail_links.csv")
    links = get_links()
    with multiprocessing.Pool(processes=8) as pool:
        data = pool.map(get_detail, links)
    write_csv(data, "output", "edu_details.csv")
