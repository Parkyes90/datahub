import csv
import os
import sys

from bs4 import BeautifulSoup

from common import DATA_DIR

csv.field_size_limit(sys.maxsize)

if __name__ == "__main__":
    ret = []
    columns = ["index", "year", "title", "category", "context"]
    result_path = os.path.join(DATA_DIR, "output", "results.csv")
    with open(result_path) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 17698:
                continue
            if i == 18000:
                break
            if i == 0:
                continue
            index, year, title, category, context = row
            temp = {
                "index": index,
                "year": year,
                "title": title,
                "category": category,
                "context": context,
            }
            soup = BeautifulSoup(context, "html.parser")
            print(soup.text)
            for column in columns:
                if not temp[column].startswith('"'):
                    temp[column] = f'"{temp[column]}'
                if not temp[column].endswith('"'):
                    temp[column] = f'{temp[column]}"'

            ret.append(temp)
