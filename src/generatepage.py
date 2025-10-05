import os
from converter import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            heading = line.split("# ", maxsplit=1)[-1].strip()
            return heading
    raise ValueError("No h1 found")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as input_file:
        markdown = input_file.read()

    with open(template_path) as template_file:
        html_template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    final_html = html_template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_node.to_html()
    )

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as output_file:
        output_file.write(final_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for location in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, location)
        if os.path.isfile(path):
            current_main, current_ext = os.path.splitext(location)
            if current_ext == ".md":
                dest = os.path.join(dest_dir_path, "".join([current_main, ".html"]))
                generate_page(path, template_path, dest)
        if os.path.isdir(path):
            dest = os.path.join(dest_dir_path, location)
            os.mkdir(dest)
            generate_pages_recursive(path, template_path, dest)
