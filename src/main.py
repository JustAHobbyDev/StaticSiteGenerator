from pathlib import Path
from generator import del_dir_children, generate_page_recursive
import shutil

class Config:
    template_path = 'template.html'

def build(source, target):
    generate_page_recursive(source, Config.template_path, target)

def recursive_copy(source, target):
    source, target = Path(source), Path(target)
    for child in source.iterdir():
        target_child = target / child.name
        if child.is_dir():
            print(f'Copying directory {child} to {target / child.name}')
            target_child.mkdir()
            print(f'recursive_copy({child}, {target / child.name})')
            print("---\n")
            recursive_copy(child, target_child)
        if child.is_file():
            print(f'Copying file {child.name} to {target_child}')
            shutil.copy(child, target)
            print("---\n")


if __name__ == '__main__':
    del_dir_children('public')
    build('content', 'public')
    recursive_copy('static', 'public')