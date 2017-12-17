import glob
import os
from PyPDF2 import PdfFileMerger, PdfFileWriter

pdfs = os.listdir("./uploads/")
print(pdfs)
merger = PdfFileMerger()
for pdf in pdfs:
    merger.append("./uploads/" + pdf)
with open('result.pdf', 'wb') as fout:
    merger.write(fout)
