# CV Maker

A simple resume beautification tool that takes raw resume content (PDF, Word, or TXT) and generates a styled PDF based on custom Figma designs.

## Features

- PDF text extraction and parsing
- Modern web interface with Tailwind CSS
- Direct text editing in browser
- High-quality PDF generation
- Automatic language detection (English/Chinese)
- Local processing (no data sent to servers)

## System Dependencies

### macOS
Using Homebrew:
```bash
brew install pango libffi cairo pkg-config gtk+3 gobject-introspection
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev
```

### Windows
1. Install GTK3 runtime using [MSYS2](https://www.msys2.org/)
2. Add GTK3 binary path to system PATH
3. Install the required packages:
```bash
pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-pip mingw-w64-x86_64-python3-cffi
```

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
# On macOS/Linux
./run.sh

# On Windows
python CVMaker.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Upload your resume (PDF, DOCX, or TXT format)
2. Wait for the content to be extracted and displayed
3. Edit the content directly in the browser if needed
4. Click "Download PDF" to generate the styled version

## Project Structure

```
CVMaker/
├── CVMaker.py          # Main application file
├── run.sh             # Run script with environment variables
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   └── index.html    # Main web interface
├── data/             # Sample data and templates
└── output/           # Generated PDFs
```

## Dependencies

- Flask: Web framework
- pdfplumber: PDF text extraction
- WeasyPrint: PDF generation
- langdetect: Language detection
- Tailwind CSS: Styling (via CDN)

## Notes

- Maximum file size: 10MB
- Supported formats: PDF, DOCX, TXT
- Supported languages: English, Chinese 

## Update
As a lot of issues happened for online customizing the component and text in CV, I decided to use Figma to design the CV template and then convert it to HTML + Tailwind CSS. But finally, CV needs to be exported as a PDF file. Then seems like there is no need to convert to HTML + Tailwind CSS. Further there is no need to develop this tool. 

Pending now for further development while I have any new idea about the CV maker.