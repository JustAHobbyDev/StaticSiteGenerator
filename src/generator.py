import os
from pathlib import Path
from markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    from_path = Path(from_path)
    if not from_path.exists():
        raise FileNotFoundError(f'{from_path.name} not found')
    
    with open(from_path) as f:
        markdown = f.read()

    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f'{template_path.name} not found')

    print(f'Opening {template_path}...')
    with open(template_path) as f:
        template_file = f.read()
        
    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()
    title = extract_title(markdown)
    title_template_parts = template_file.split('{{ Title }}')
    template_with_title = title_template_parts[0] + title + title_template_parts[1]
    content_template_parts = template_with_title.split('{{ Content }}')
    template_with_content = content_template_parts[0] + html + content_template_parts[1]

    # Check `dest_path` exists
    # Create `dest_path` if not\
    dest_path = Path(dest_path)
    if not dest_path.parent.exists():
        print(f'dest_path.parent: {dest_path.parent}')
        print(f'Making {dest_path.parent}...')
        dest_path.parent.mkdir()
    # remove old generated file
    print(f'Cleaning {dest_path}...')
    dest_path.unlink(missing_ok=True)
    # Write the html page to a file at `dest_path`
    print(f'Opening {dest_path}...')
    with open(dest_path, 'w', encoding="utf-8") as dest_file:
        print(f'Writing {dest_path}...')
        dest_file.write(template_with_content)
    
    print("All done!")

    
# if __name__ == '__main__':
#     generate_page(from)