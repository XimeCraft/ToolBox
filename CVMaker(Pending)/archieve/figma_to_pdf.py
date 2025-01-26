import json
import os
from jinja2 import Environment, FileSystemLoader
import weasyprint
from pathlib import Path

class FigmaConverter:
    def __init__(self, json_path, template_dir='templates'):
        self.json_path = json_path
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def load_figma_data(self):
        """Load and parse Figma JSON data"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def extract_text_content(self, node):
        """Recursively extract text content from Figma nodes"""
        content = {}
        
        if node.get('type') == 'TEXT':
            # Extract text content and styles
            content['text'] = node.get('characters', '')
            content['style'] = {
                'fontFamily': node.get('style', {}).get('fontFamily', 'Inter'),
                'fontSize': node.get('style', {}).get('fontSize', 16),
                'fontWeight': node.get('style', {}).get('fontWeight', 400),
                'textCase': node.get('style', {}).get('textCase', 'none')
            }
            
        # Recursively process child nodes
        if 'children' in node:
            for child in node['children']:
                child_content = self.extract_text_content(child)
                if child_content:
                    # Merge child content with current content
                    content.update(child_content)
                    
        return content
        
    def generate_html(self, output_path):
        """Generate HTML from Figma data"""
        data = self.load_figma_data()
        
        # Extract content from Figma data
        content = self.extract_text_content(data['document'])
        
        # Load template
        template = self.env.get_template('resume_template.html')
        
        # Render HTML
        html = template.render(content=content)
        
        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        return output_path
        
    def generate_pdf(self, html_path, pdf_path):
        """Convert HTML to PDF"""
        # Create PDF from HTML
        html = weasyprint.HTML(filename=html_path)
        html.write_pdf(pdf_path)
        
        return pdf_path

def main():
    # Setup paths
    current_dir = Path(__file__).parent
    json_path = current_dir / 'figma_data.json'
    
    html_path = current_dir / 'resume.html'
    pdf_path = current_dir / 'resume.pdf'
    
    # Initialize converter
    converter = FigmaConverter(json_path)
    
    # Generate HTML
    print(f"Generating HTML file: {html_path}")
    converter.generate_html(html_path)
    
    # Generate PDF
    print(f"Generating PDF file: {pdf_path}")
    converter.generate_pdf(html_path, pdf_path)
    
    print("Conversion completed successfully!")

if __name__ == '__main__':
    main() 