import csv
import os
import time

from selenium import webdriver

from common import BASE_DIR, CATEGORY, write_csv, options, DATA_DIR

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

    for idx, link in enumerate(links):
        print(idx)
        d = webdriver.Chrome(
            os.path.join(BASE_DIR, "chromedriver"), options=options
        )
        d.get(link)
        y = d.find_element_by_xpath(
            "/html/head/meta[@property='og:createdate']"
        )
        y = y.get_attribute("content")
        y = y.split(".")[0]
        context = d.find_element_by_tag_name("body").text
        title = d.title
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


def change_column():
    ret = []
    with open(os.path.join(DATA_DIR, "output", "edu_blog.csv")) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            title, year, context, category = row
            ret.append(
                {
                    "year": year,
                    "title": title,
                    "category": category,
                    "context": context,
                }
            )
    return ret


if __name__ == "__main__":
    data = change_column()
    # data = get_all_list()
    write_csv(data, "output", "edu_blog.csv")
