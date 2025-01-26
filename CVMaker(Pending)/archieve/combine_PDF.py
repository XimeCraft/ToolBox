from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("Page1.pdf")
merger.append("Page2.pdf")
merger.write("Final_CV.pdf")
merger.close()