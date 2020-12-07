import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from common import BASE_DIR, CATEGORY, write_csv

driver = webdriver.Chrome(os.path.join(BASE_DIR, "chromedriver"))


def get_all_list():
    ret = []
    url = (
        "https://post.naver.com"
        "/search/authorPost.nhn"
        "?keyword=미래+교육&memberNo=15194331&fromNo=2&sortType="
    )
    blacklist = {
        "[document]",
        "noscript",
        "header",
        "html",
        "meta",
        "head",
        "input",
        "script",
        # there may be more elements you don't want, such as "style", etc.
    }
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)
    more = driver.find_element_by_css_selector("#more_btn")
    more.click()
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    posts = driver.find_elements_by_class_name("link_end")
    links = set()
    for post in posts:
        links.add(post.get_attribute("href"))
    driver.close()

    for link in list(links):
        d = webdriver.Chrome(os.path.join(BASE_DIR, "chromedriver"))
        d.get(link)
        y = d.find_element_by_xpath(
            "/html/head/meta[@property='og:createdate']"
        )
        y = y.get_attribute("content")
        y = y.split(".")[0]
        context = d.find_element_by_tag_name("body").text
        title = d.find_element_by_tag_name("title").text
        d.close()
        ret.append(
            {
                "title": title,
                "year": y,
                "context": context,
                "category": CATEGORY,
            }
        )

    return ret


if __name__ == "__main__":
    data = get_all_list()
    write_csv(data, "output", "edu_blog.csv")
