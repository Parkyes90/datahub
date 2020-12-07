import os
import re
import pdftotext

from common import FORMAT_STRING, CATEGORY, write_csv, DATA_DIR


def get_pdf_files():
    ret = []
    keris_data_dir = os.path.join(DATA_DIR, "keris")
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
                "category": CATEGORY,
                "context": text,
            }
        )
        # print(filename.split("."))
    write_csv(ret, "output", "keris.csv")
