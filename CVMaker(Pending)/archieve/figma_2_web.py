import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

FIGMA_ACCESS_TOKEN = os.getenv('FIGMA_ACCESS_TOKEN')
FILE_ID = os.getenv('FIGMA_FILE_KEY')

def get_figma_data(file_id):
    """ 从 Figma API 获取设计数据 """
    headers = {"X-Figma-Token": FIGMA_ACCESS_TOKEN}
    url = f"https://api.figma.com/v1/files/{file_id}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open("figma_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ JSON 导出成功！")
    else:
        print(f"❌ 错误：{response.status_code} - {response.text}")
        

def parse_node(node):
    """ 解析 Figma JSON 结构并转换为 HTML """
    html = ""

    # 处理 Frame（页面容器）
    if node["type"] == "FRAME":
        html += '<div class="bg-white p-6 rounded-lg shadow-md mb-4">\n'
        for child in node.get("children", []):
            html += parse_node(child)  # 递归解析子元素
        html += '</div>\n'

    # 处理 Text（文本）
    elif node["type"] == "TEXT":
        text = node.get("characters", "").replace("\n", "<br>")
        font_size = node.get("style", {}).get("fontSize", 16)
        if font_size > 20:
            html += f'<h1 class="text-xl font-bold text-gray-700">{text}</h1>\n'
        else:
            html += f'<p class="text-lg text-gray-600">{text}</p>\n'

    # 处理 Rectangle（背景颜色）
    elif node["type"] == "RECTANGLE":
        fills = node.get("fills", [])
        bg_color = "bg-gray-200"  # 默认颜色
        if fills and "color" in fills[0]:
            r, g, b = fills[0]["color"]["r"], fills[0]["color"]["g"], fills[0]["color"]["b"]
            bg_color = f'bg-[rgb({int(r*255)},{int(g*255)},{int(b*255)})]'
        html += f'<div class="{bg_color} p-4 rounded-md"></div>\n'

    return html

def generate_html_from_figma(figma_json):
    """ 生成 HTML + Tailwind CSS """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Figma to HTML</title>
    </head>
    <body class="bg-gray-100 p-4">
    """

    # 获取 Canvas 层级
    canvas = figma_json["document"]["children"][0]  # 选取第一个 Canvas
    if "children" in canvas:
        for node in canvas["children"]:
            html_content += parse_node(node)

    html_content += """
    </body>
    </html>
    """

    with open("CVMaker/output/output.html", "w") as f:
        f.write(html_content)

    print("✅ HTML 生成成功：output.html")


if __name__ == "__main__":
    get_figma_data(FILE_ID)
    with open("figma_data.json", "r", encoding="utf-8") as f:
        figma_data = json.load(f)
    if figma_data:
        generate_html_from_figma(figma_data)