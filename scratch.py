from pdfminer.high_level import extract_pages
import os
import pandas as pd

# check out all invoices
directory = os.fsencode('data')

for _file in os.listdir(directory):
    filename = os.fsdecode(_file)
    for page in extract_pages('data/' + filename):
        print(len(page))
        for element in page:
            try:
                print(element.get_text())
            except:
                pass
        print("--------------------------------------------------------")
