import csv
import multiprocessing
import os


from selenium import webdriver

from common import BASE_DIR, write_csv, options, DATA_DIR, CATEGORY

href = ""


def write_link(page):
    ret = []
    driver = webdriver.Chrome(
        os.path.join(BASE_DIR, "chromedriver"), options=options
    )
    print(page)
    url = (
        f"http://www.eduinnews.co.kr"
        f"/news/articleList.html"
        f"?page={page}"
        f"&total=285"
        f"&sc_area=A"
        f"&view_type=sm"
        f"&sc_word=%EB%AF%B8%EB%9E%98+%EA%B5%90%EC%9C%A1"
    )
    driver.get(url)

    posts = driver.find_elements_by_css_selector(".list-block")

    for post in posts:
        title = post.find_element_by_tag_name("strong").text
        year = post.find_element_by_class_name("list-dated").text.split("|")
        year = year[len(year) - 1].split("-")[0].replace(" ", "")
        link = post.find_element_by_tag_name("a").get_attribute("href")
        ret.append({"year": year, "title": title, "link": link})
    driver.close()
    return ret


def detail(r):
    idx, year, title, link = r
    print(idx)
    driver = webdriver.Chrome(
        os.path.join(BASE_DIR, "chromedriver"), options=options
    )
    driver.get(link)
    context = driver.find_element_by_tag_name("body").text
    driver.close()
    return {
        "year": year,
        "title": title,
        "category": CATEGORY,
        "context": context,
    }


def get_links():
    ret = []
    with open(os.path.join(DATA_DIR, "output", "edu_in_news_list.csv")) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            ret.append([idx, *row])
            # year, link = row
    return ret


if __name__ == "__main__":
    links = get_links()
    with multiprocessing.Pool(processes=8) as pool:
        data = pool.map(detail, links)
    # ret = []
    # for item in data:
    #     for record in item:
    #         ret.append(record)
    write_csv(data, "output", "edu_in_news.csv")
