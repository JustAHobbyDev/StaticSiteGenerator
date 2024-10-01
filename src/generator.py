import os
from pathlib import Path
from markdown import markdown_to_html_node, extract_title


def del_dir_children(path):
    path = Path(path)
    for fd in path.iterdir():
        if fd.is_file():
            fd.unlink()
    
    for _dir in path.iterdir():
        if _dir.iterdir():
            del_dir_children(_dir)
        _dir.rmdir()
        

def generate_page_recursive(from_path, template_path, dest_path):
    from_entries = Path().glob(f'{from_path}/**/*')
    for from_entry in from_entries:
        str_from_entry = str(from_entry)
        str_dest_entry = str_from_entry.replace(from_path, dest_path)
        str_dest_entry = str_dest_entry.replace('.md', '.html')
        dest_entry = Path(str_dest_entry)
        if from_entry.is_dir():
            dest_entry.mkdir
        if from_entry.is_file():
            generate_page(from_entry, template_path, dest_entry)



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
    # print(f'\nhtml_nodes: [{html_nodes}]\n')
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
    # Write the html page to a file at `dest_path`
    print(f'Opening {dest_path}...')
    with open(dest_path, 'w', encoding="utf-8") as dest_file:
        print(f'Writing {dest_path}...')
        dest_file.write(template_with_content)
    
    print("All done!")

    
if __name__ == '__main__':
#  generate_page(from)
    # d = generate_pages_recursive('content')
    # del_dir_children('public')
    generate_page_recursive('content', 'template.html', 'public')