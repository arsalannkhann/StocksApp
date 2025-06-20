import os

def print_tree(start_path='.', prefix=''):
    entries = sorted(os.listdir(start_path))
    for i, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        connector = '└── ' if i == len(entries) - 1 else '├── '
        print(prefix + connector + entry)
        if os.path.isdir(path):
            extension = '    ' if i == len(entries) - 1 else '│   '
            print_tree(path, prefix + extension)

if __name__ == '__main__':
    root_dir = os.path.abspath('.')
    print(f"Project structure for: {root_dir}\n")
    print_tree(root_dir)