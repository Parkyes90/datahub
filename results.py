import csv
import os
import sys


from common import DATA_DIR, write_csv

csv.field_size_limit(sys.maxsize)

if __name__ == "__main__":
    ret = []
    columns = ["year", "title", "category", "context"]
    result_path = os.path.join(DATA_DIR, "output", "results.csv")
    with open(result_path) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue

            index, year, title, category, context = row
            # index = index.replace('"', "")
            # year = f"{year}"
            # title = title.replace('"', "")
            # category = category.replace('"', "")
            context = context.replace(" ", " ").replace("​", " ")
            temp = {
                "index": index,
                "year": year,
                "title": title,
                "category": category,
                "context": context,
            }
            for column in columns:
                if not temp[column].startswith('"'):
                    temp[column] = f'"{temp[column]}'
                if not temp[column].endswith('"'):
                    temp[column] = f'{temp[column]}"'

            ret.append(temp)

    # print(ret[0])
    write_csv(ret, "output", "results.csv")
