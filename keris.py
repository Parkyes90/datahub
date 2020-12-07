import os
import re
import pdftotext
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent

FORMAT_STRING = r"\d{4}-\d\d?"


def get_pdf_files():
    ret = []
    data_dir = os.path.join(BASE_DIR, "data")
    keris_data_dir = os.path.join(data_dir, "keris")
    files = os.listdir(keris_data_dir)
    for filename in files:
        print(f"{filename} read start")
        p = re.compile(FORMAT_STRING)
        remain = p.split(filename)
        date = p.search(filename).group()
        title = remain[1].split(".pdf")[0]
        title = title.replace(" ", "", 1).replace("_", "", 1)
        file = open(os.path.join(keris_data_dir, filename), "rb")
        pdf_reader = pdftotext.PDF(file)
        text = ""
        for page in pdf_reader:
            text += page
        ret.append(
            {
                "year": date.split("-")[0],
                "title": title,
                "category": "일반문서",
                "context": text,
            }
        )
        # print(filename.split("."))
    with open(os.path.join(data_dir, "output", "keris.csv"), "w") as f:
        w = csv.writer(f)
        w.writerow(ret[0].keys())
        for r in ret:
            w.writerow(r.values())
