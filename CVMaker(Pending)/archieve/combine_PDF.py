from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("/Users/xiao/Projects/git/ToolBox/CVMaker(Pending)/data/Eng.pdf")
merger.append("/Users/xiao/Projects/git/ToolBox/CVMaker(Pending)/data/Eng2.pdf")
merger.write("/Users/xiao/Projects/git/ToolBox/CVMaker(Pending)/data/Final_CV.pdf")
merger.close()
