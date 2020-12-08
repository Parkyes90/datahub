import _csv
import csv
import multiprocessing
import os
import re
import sys

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from common import FORMAT_STRING, CATEGORY, write_csv, DATA_DIR

csv.field_size_limit(sys.maxsize)


def get_files():
    keris_data_dir = os.path.join(DATA_DIR, "keris")
    files = os.listdir(keris_data_dir)
    return [os.path.join(keris_data_dir, filename) for filename in files]


def merge_csvs():
    keris_data_dir = os.path.join(DATA_DIR, "export_pdfs")
    ret = []
    for filename in os.listdir(keris_data_dir):
        with open(os.path.join(keris_data_dir, filename)) as f:
            reader = csv.reader(f)
            try:
                for i, row in enumerate(reader):
                    if i == 0:
                        continue
                    year, title, category, context = row
                    context = context.replace("\n", " ")
                    context = re.sub(r"\(cid:\d{1,10}\)", "", context)
                    ret.append(
                        {
                            "year": year,
                            "title": title,
                            "category": category,
                            "context": context,
                        }
                    )
            except _csv.Error:
                pass
    write_csv(
        ret, "output", f"keris.csv",
    )


def get_pdf_files(filename):
    output_string = StringIO()
    print(f"{filename} read start")
    p = re.compile(FORMAT_STRING)
    remain = p.split(filename)
    date = p.search(filename).group()
    title = remain[1].split(".pdf")[0]
    title = title.replace(" ", "", 1).replace("_", "", 1)
    file = open(filename, "rb")
    parser = PDFParser(file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    text = str(output_string.getvalue())

    text = re.sub(r"\(cid:\d{1,4}\)", "", text)
    file.close()
    splited = filename.split("/")
    write_csv(
        [
            {
                "year": date.split("-")[0],
                "title": title,
                "category": CATEGORY,
                "context": text,
            }
        ],
        "export_pdfs",
        f"{splited[len(splited) - 1]}.csv",
    )


if __name__ == "__main__":
    # filenames = get_files()
    # for filename in filenames:
    #     get_pdf_files(filename)
    # with multiprocessing.Pool(
    #     processes=multiprocessing.cpu_count() * 2
    # ) as pool:
    #     pool.map(get_pdf_files, filenames)
    # write_csv(data, "output", "keris.csv")
    merge_csvs()
