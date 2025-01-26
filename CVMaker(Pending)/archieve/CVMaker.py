import os
import json
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
import pdfplumber
import weasyprint
from langdetect import detect
import jinja2
import tempfile
import time

app = Flask(__name__)

# Configure template directory
template_dir = Path(__file__).parent / 'templates'
app.jinja_loader = jinja2.FileSystemLoader(str(template_dir))

class CVMaker:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
        self.output_dir = Path(__file__).parent / 'output'
        self.output_dir.mkdir(exist_ok=True)
        self.template_dir = Path(__file__).parent / 'data'
        self.default_template = self.template_dir / 'template.fig'

    def load_figma_template(self, template_path=None):
        """Load and parse Figma template file."""
        if template_path is None:
            template_path = self.default_template

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # Extract styles and layout from Figma JSON
            styles = self.extract_figma_styles(template_data)
            return styles
        except Exception as e:
            print(f"Error loading Figma template: {str(e)}")
            return None

    def extract_figma_styles(self, template_data):
        """Extract CSS styles from Figma JSON data."""
        styles = {
            'layout': 'single-column',  # or 'two-column'
            'colors': {
                'primary': '#2563eb',
                'secondary': '#475569',
                'background': '#ffffff',
                'text': '#000000'
            },
            'typography': {
                'heading': {
                    'font-family': 'Inter',
                    'font-size': '24px',
                    'font-weight': '600'
                },
                'body': {
                    'font-family': 'Inter',
                    'font-size': '16px',
                    'font-weight': '400'
                }
            },
            'spacing': {
                'section': '2rem',
                'item': '1rem'
            }
        }
        
        # TODO: Parse actual styles from Figma JSON
        return styles

    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF file."""
        text_content = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content.append(page.extract_text())
            return '\n'.join(text_content)
        except Exception as e:
            return f"Error extracting PDF content: {str(e)}"

    def detect_language(self, text):
        """Detect if the text is in English or Chinese."""
        try:
            lang = detect(text)
            return 'zh' if lang == 'zh-cn' else 'en'
        except:
            return 'en'  # Default to English

    def parse_resume_content(self, text):
        """Parse raw text into structured JSON format."""
        sections = {
            'contact': {},
            'summary': '',
            'experience': [],
            'education': [],
            'skills': []
        }
        
        # Basic parsing logic
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Try to identify sections
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in ['contact', 'email', 'phone', 'address']):
                current_section = 'contact'
                if '@' in line:
                    sections['contact']['email'] = line
                elif any(char.isdigit() for char in line):
                    sections['contact']['phone'] = line
            elif any(keyword in lower_line for keyword in ['summary', 'objective', 'profile']):
                current_section = 'summary'
                sections['summary'] = line
            elif any(keyword in lower_line for keyword in ['experience', 'work', 'employment']):
                current_section = 'experience'
            elif any(keyword in lower_line for keyword in ['education', 'academic']):
                current_section = 'education'
            elif any(keyword in lower_line for keyword in ['skills', 'technologies', 'tools']):
                current_section = 'skills'
            elif current_section:
                if current_section == 'experience':
                    sections['experience'].append(line)
                elif current_section == 'education':
                    sections['education'].append(line)
                elif current_section == 'skills':
                    sections['skills'].append(line)
                elif current_section == 'summary':
                    sections['summary'] += ' ' + line
        
        return sections

    def generate_pdf(self, html_content, output_path=None):
        """Generate PDF from HTML content."""
        try:
            if output_path is None:
                output_path = self.output_dir / f"resume_{int(time.time())}.pdf"
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding='utf-8', delete=False) as f:
                f.write(html_content)
                temp_html = f.name

            # Generate PDF
            weasyprint.HTML(filename=temp_html).write_pdf(output_path)
            
            # Clean up temporary file
            os.unlink(temp_html)
            
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    cv_maker = CVMaker()
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(file.filename)[1], delete=False) as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        # Extract and process content
        content = cv_maker.extract_text_from_pdf(temp_path)
        language = cv_maker.detect_language(content)
        structured_data = cv_maker.parse_resume_content(content)

        # Load template styles
        template_styles = cv_maker.load_figma_template()

        return jsonify({
            'content': content,
            'language': language,
            'structured_data': structured_data,
            'template_styles': template_styles
        })
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        content = data.get('content', '')
        template_styles = data.get('template_styles', {})
        
        cv_maker = CVMaker()
        
        # Create HTML content with template styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                :root {{
                    --primary-color: {template_styles.get('colors', {}).get('primary', '#2563eb')};
                    --secondary-color: {template_styles.get('colors', {}).get('secondary', '#475569')};
                    --background-color: {template_styles.get('colors', {}).get('background', '#ffffff')};
                    --text-color: {template_styles.get('colors', {}).get('text', '#000000')};
                }}
                
                body {{
                    font-family: {'"Noto Sans SC"' if data.get('language') == 'zh' else '"Inter"'}, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: var(--background-color);
                    color: var(--text-color);
                }}
                
                h1, h2, h3 {{
                    color: var(--primary-color);
                    margin-top: {template_styles.get('spacing', {}).get('section', '2rem')};
                    margin-bottom: {template_styles.get('spacing', {}).get('item', '1rem')};
                }}
                
                section {{
                    margin-bottom: {template_styles.get('spacing', {}).get('section', '2rem')};
                }}
                
                pre {{
                    white-space: pre-wrap;
                    font-family: inherit;
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """
        
        # Generate PDF
        output_path = cv_maker.generate_pdf(html_content)
        if output_path:
            return send_file(str(output_path), as_attachment=True, download_name='resume.pdf')
        else:
            return jsonify({'error': 'Failed to generate PDF'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
