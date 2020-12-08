import csv
import os
import sys

from common import write_csv, DATA_DIR

csv.field_size_limit(sys.maxsize)


def merge():
    ret = []
    files = os.listdir(os.path.join(DATA_DIR, "output"))
    idx = 1
    for file in files:
        with open(os.path.join(DATA_DIR, "output", file)) as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                year, title, category, context = row
                ret.append(
                    {
                        "index": idx,
                        "year": year,
                        "title": title,
                        "category": category,
                        "context": context,
                    }
                )
                idx += 1
    print(ret)
    return ret


if __name__ == "__main__":
    data = merge()
    write_csv(data, "output", "results.csv")
