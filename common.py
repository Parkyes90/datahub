import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CATEGORY = "일반문서"
FORMAT_STRING = r"\d{4}-\d\d?"
DATA_DIR = os.path.join(BASE_DIR, "data")


def write_csv(ret, dirname, filename):
    with open(os.path.join(DATA_DIR, dirname, filename), "w") as f:
        w = csv.writer(f)
        w.writerow(ret[0].keys())
        for r in ret:
            w.writerow(r.values())
