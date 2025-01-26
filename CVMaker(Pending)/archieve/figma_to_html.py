import os
import json
import requests
from pathlib import Path
import argparse
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

access_token = os.getenv('FIGMA_ACCESS_TOKEN')
file_key = os.getenv('FIGMA_FILE_KEY')

class FigmaToHTML:
    def __init__(self, access_token=None):
        self.access_token = access_token or os.getenv('FIGMA_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("Figma access token is required. Set it in .env file or pass it as an argument.")
        
        self.headers = {
            'X-Figma-Token': self.access_token
        }
        self.base_url = 'https://api.figma.com/v1'

    def get_file(self, file_key):
        """Get Figma file data."""
        url = f'{self.base_url}/files/{file_key}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_node(self, file_key, node_id):
        """Get specific node from Figma file."""
        url = f'{self.base_url}/files/{file_key}/nodes?ids={node_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def extract_styles(self, node):
        """Extract styles from Figma node."""
        styles = {
            'layout': self._get_layout_type(node),
            'colors': self._extract_colors(node),
            'typography': self._extract_typography(node),
            'spacing': self._extract_spacing(node)
        }
        return styles

    def _get_layout_type(self, node):
        """Determine if layout is single or two-column."""
        if node.get('layoutMode') == 'HORIZONTAL':
            return 'two-column'
        return 'single-column'

    def _extract_colors(self, node):
        """Extract color information from node."""
        colors = {
            'primary': '#2563eb',
            'secondary': '#475569',
            'background': '#ffffff',
            'text': '#000000'
        }
        
        if node.get('fills'):
            for fill in node['fills']:
                if fill.get('type') == 'SOLID':
                    color = fill.get('color', {})
                    # Convert RGB (0-1) to hex
                    hex_color = '#{:02x}{:02x}{:02x}'.format(
                        int(color.get('r', 0) * 255),
                        int(color.get('g', 0) * 255),
                        int(color.get('b', 0) * 255)
                    )
                    # Try to determine color role
                    if fill.get('name', '').lower().startswith('primary'):
                        colors['primary'] = hex_color
                    elif fill.get('name', '').lower().startswith('secondary'):
                        colors['secondary'] = hex_color
                    elif fill.get('name', '').lower().startswith('background'):
                        colors['background'] = hex_color
                    elif fill.get('name', '').lower().startswith('text'):
                        colors['text'] = hex_color
        
        return colors

    def _extract_typography(self, node):
        """Extract typography information from node."""
        typography = {
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
        }
        
        if node.get('style'):
            style = node['style']
            font_family = style.get('fontFamily', 'Inter')
            font_size = f"{style.get('fontSize', 16)}px"
            font_weight = str(style.get('fontWeight', 400))
            
            if style.get('textStyleId', '').lower().startswith('heading'):
                typography['heading'].update({
                    'font-family': font_family,
                    'font-size': font_size,
                    'font-weight': font_weight
                })
            else:
                typography['body'].update({
                    'font-family': font_family,
                    'font-size': font_size,
                    'font-weight': font_weight
                })
        
        return typography

    def _extract_spacing(self, node):
        """Extract spacing information from node."""
        spacing = {
            'section': '2rem',
            'item': '1rem'
        }
        
        if node.get('itemSpacing'):
            spacing['item'] = f"{node['itemSpacing'] / 16}rem"
        if node.get('paddingTop'):
            spacing['section'] = f"{node['paddingTop'] / 16}rem"
        
        return spacing

    def generate_html_template(self, styles):
        """Generate HTML template with Tailwind CSS classes."""
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '{styles['colors']['primary']}',
                        secondary: '{styles['colors']['secondary']}',
                    }},
                    fontFamily: {{
                        sans: ['{styles['typography']['body']['font-family']}', 'system-ui', 'sans-serif'],
                    }},
                }}
            }}
        }}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family={styles['typography']['body']['font-family'].replace(' ', '+')}&display=swap');
        
        .resume-heading {{
            font-size: {styles['typography']['heading']['font-size']};
            font-weight: {styles['typography']['heading']['font-weight']};
        }}
        
        .resume-body {{
            font-size: {styles['typography']['body']['font-size']};
            font-weight: {styles['typography']['body']['font-weight']};
        }}
        
        .section-spacing {{
            margin-bottom: {styles['spacing']['section']};
        }}
        
        .item-spacing {{
            margin-bottom: {styles['spacing']['item']};
        }}
    </style>
</head>
<body class="bg-{styles['colors']['background']} text-{styles['colors']['text']} p-8">
    <div class="max-w-4xl mx-auto {styles['layout']}">
        <!-- Header Section -->
        <header class="section-spacing">
            <h1 class="resume-heading text-primary">Your Name</h1>
            <p class="resume-body text-secondary">Professional Title</p>
        </header>

        <!-- Contact Section -->
        <section class="section-spacing">
            <h2 class="resume-heading text-primary">Contact</h2>
            <div class="resume-body item-spacing">
                <p>email@example.com</p>
                <p>+1 234 567 890</p>
            </div>
        </section>

        <!-- Experience Section -->
        <section class="section-spacing">
            <h2 class="resume-heading text-primary">Experience</h2>
            <div class="resume-body">
                <div class="item-spacing">
                    <h3 class="font-semibold">Company Name</h3>
                    <p class="text-secondary">Position • 2020 - Present</p>
                    <ul class="list-disc list-inside mt-2">
                        <li>Achievement or responsibility</li>
                        <li>Achievement or responsibility</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- Education Section -->
        <section class="section-spacing">
            <h2 class="resume-heading text-primary">Education</h2>
            <div class="resume-body">
                <div class="item-spacing">
                    <h3 class="font-semibold">University Name</h3>
                    <p class="text-secondary">Degree • 2016 - 2020</p>
                </div>
            </div>
        </section>

        <!-- Skills Section -->
        <section class="section-spacing">
            <h2 class="resume-heading text-primary">Skills</h2>
            <div class="resume-body">
                <ul class="list-disc list-inside">
                    <li>Skill 1</li>
                    <li>Skill 2</li>
                    <li>Skill 3</li>
                </ul>
            </div>
        </section>
    </div>
</body>
</html>"""
        return template

def main():
    parser = argparse.ArgumentParser(description='Convert Figma design to HTML + Tailwind CSS')
    parser.add_argument('--token', help='Figma access token (optional if set in .env)')
    parser.add_argument('--file', help='Figma file key (optional if set in .env)')
    parser.add_argument('--node', help='Specific node ID (optional)')
    parser.add_argument('--output', default='template.html', help='Output HTML file name')
    
    args = parser.parse_args()
    
    try:
        converter = FigmaToHTML(args.token)
        
        # Get file key from args or environment
        file_key = args.file or os.getenv('FIGMA_FILE_KEY')
        if not file_key:
            raise ValueError("Figma file key is required. Set it in .env file or pass it as an argument.")
        
        # Get Figma file data
        file_data = converter.get_file(file_key)
        
        # Get specific node or use document
        if args.node:
            node_data = converter.get_node(file_key, args.node)
            styles = converter.extract_styles(node_data['nodes'][args.node])
        else:
            styles = converter.extract_styles(file_data['document'])
        
        # Generate HTML
        html = converter.generate_html_template(styles)
        
        # Save to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'Generated HTML template: {args.output}')
        print('Styles extracted:', json.dumps(styles, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 