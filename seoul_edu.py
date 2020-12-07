import requests
from bs4 import BeautifulSoup

from common import write_csv, CATEGORY


def get_detail(article, cache):
    detail = requests.get(article.a.get("href"))
    detail_soup = BeautifulSoup(detail.text, "html.parser")
    year = detail_soup.select("a.post__cat.cat-theme")
    year = year[1].text.split(" ")[0]
    try:
        cache["current_year"] = int(year)
    except ValueError:
        pass
    title = detail_soup.select("h1.entry-title.entry-title--lg")
    title = title[0].text
    contexts = detail_soup.select("div.container.container--narrow p")
    context = ""
    for c in contexts:
        context += c.text
    print(cache["current_year"])
    return {
        "year": cache["current_year"],
        "title": title,
        "category": CATEGORY,
        "context": context,
    }


def get_all_list():
    ret = []
    cache = {"current_year": 2020}
    response = requests.get("http://webzine-serii.re.kr?s=미래+교육")
    soup = BeautifulSoup(response.text, "html.parser")
    pages = soup.select(".mnmd-pagination__item")
    maximum = 0
    articles = soup.select("h3.post__title.typescale-2")
    for article in articles:
        ret.append(get_detail(article, cache))
        # print(detail_soup)
    for page in pages:
        try:
            p = int(page.text)
            maximum = max(p, maximum)
        except ValueError:
            pass
    for page in range(1, maximum):
        print(f"now {page+1}")
        url = f"http://webzine-serii.re.kr/page/{page+1}/?s=미래+교육"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("h3.post__title.typescale-2")
        for article in articles:
            ret.append(get_detail(article, cache))
    return ret


if __name__ == "__main__":
    data = get_all_list()
    write_csv(data, "output", "seoul_edu.csv")
