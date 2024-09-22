from pathlib import Path
import shutil

def build(source, target):
    root = Path.cwd()
    src_dir = root / source
    target = root / target
    shutil.rmtree(target)
    target.mkdir()
    recursive_copy(src_dir, target)


def recursive_copy(source, target):

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
    build('static', 'public')