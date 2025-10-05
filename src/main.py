import os
import shutil
from generatepage import generate_pages_recursive


def main():
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def copy_directory(source_dir: str, dest_dir: str) -> None:
    print(f"deleting contents of {dest_dir}")
    delete_contents(dest_dir)
    print(f"copying contents from {source_dir}")
    copy_contents_h(source_dir, dest_dir)


def copy_contents_h(current_dir: str, dest_dir: str) -> None:
    print(current_dir)
    for location in os.listdir(current_dir):
        path = os.path.join(current_dir, location)
        dest = os.path.join(dest_dir, location)
        if os.path.isfile(path):
            shutil.copy(path, dest)
        if os.path.isdir(path):
            os.mkdir(dest)
            copy_contents_h(path, dest)


def delete_contents(current_dir: str):
    for location in os.listdir(current_dir):
        path = os.path.join(current_dir, location)
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            shutil.rmtree(path)


main()
