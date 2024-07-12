import yaml, os
import typing as t
from argparse import ArgumentParser

"""
    Create directories and its sub_directories content by using  dictionnary.
    The scripts use a .yaml file where the structure is given.
    Here is en example of .yaml file content that can be used.
    advanced data structure:
    - linked list
    - skip list
    sorting algorithms:
    - bubble sort

    This scripts keep creating directories for any sub dictionnary.

    Note that you can add .gitkeep if you need git to take account of your
    folders during commits. I added it as i need to have a my project folders
    structure in git as I progress
"""

def create_dir(name: str) -> None:
    print(f"Create dir: {name}")
    os.makedirs(name, exist_ok=True)

def add_gitkeep(path: str) -> None:
    # * can be .DS_Store
    with open(os.path.join(path, ".gitkeep"), 'w') as f:
        pass

def get_paths(path: str) -> t.List[str]:
    path_split = path.split('.')
    paths = [path_split[0]]
    for name in path_split[1:]:
        paths.append(f"{paths[-1]}/{name}")
    return paths

def get_struct(content: dict) -> t.List[str]:
    paths = []
    current = content
    for idx, key in enumerate(current):
        for sub_idx, item in enumerate(current[key]):
            if isinstance(item, dict):
                paths.extend([f"{idx+1}-{key}.{name}" for name in get_struct(item)])
                # paths.extend([f"{key}.{sub_idx_+1}-{name}" for sub_idx_, name in enumerate(get_struct(item))])
            else: paths.append(f"{idx+1}-{key}.{sub_idx+1}-{item}")
    return paths

def create_dirs_from_structure(structure: t.List[str], base_dir: str, gitkeep: bool) -> None:
    paths = set()
    if base_dir!= ".": create_dir(base_dir)
    for path in structure:
        paths.update(get_paths(path))
    for name in paths:
        name = os.path.join(base_dir, name.replace(' ', '-')).lower()
        create_dir(name)
        if gitkeep: add_gitkeep(name)
    print("Directories have been created in ")

def main(args):
    with open(args.file, 'r') as f:
        content = yaml.safe_load(f)
    create_dirs_from_structure(get_struct(content), args.dir, args.gitkeep)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True,
                        help=".yaml filename containing the structure of your project.")
    parser.add_argument("-d", "--dir", type=str, required=True, default='.',
                        help="The directory in which you want to add that structure of directory. pwd or . is the default value")
    parser.add_argument("--gitkeep", action="store_true",
                        help="Weither or not to add .gitkeep file intop each directory and sub directory.")
    args = parser.parse_args()
    main(args)