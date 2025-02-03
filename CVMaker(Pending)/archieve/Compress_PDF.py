import subprocess

def compress_pdf(input_file, output_file, pdf_setting="/screen"):
    """
    使用 Ghostscript 压缩 PDF 文件

    参数：
        input_file (str): 输入 PDF 文件路径
        output_file (str): 输出压缩后的 PDF 文件路径
        pdf_setting (str): 压缩质量设置，
                           可选值："/screen"（最低质量，适合屏幕显示）、
                                  "/ebook"、
                                  "/printer"、
                                  "/prepress"（最高质量）
    """
    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={pdf_setting}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_file}",
        input_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"PDF 压缩成功，保存为：{output_file}")
    except subprocess.CalledProcessError as e:
        print("压缩 PDF 时出错：", e)
    except FileNotFoundError:
        print("未找到 Ghostscript，请确认已安装并将其添加到 PATH 中。")

if __name__ == '__main__':
    # 指定要压缩的 PDF 文件和输出文件
    input_pdf = "/Users/xiao/Projects/git/ToolBox/CVMaker(Pending)/data/Data Scientist - Xiao MENG.pdf"
    output_pdf = "/Users/xiao/Projects/git/ToolBox/CVMaker(Pending)/data/Data Scientist - Xiao MENG_compressed.pdf"
    
    # 调用函数进行压缩，pdf_setting 参数可根据需求调整（如 "/ebook", "/printer", "/prepress"）
    compress_pdf(input_pdf, output_pdf, pdf_setting="/screen")
