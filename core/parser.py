# core/parser.py

import os
from core.utillls import load_config
from core.utillls import is_ignored_file, read_file_safely

CONFIG = load_config()


def parse_repo(repo_path):
    parsed_docs = []
    ignore_paths = CONFIG['ignore_paths']

    for root, _, files in os.walk(repo_path):
        if any(ignored in root for ignored in ignore_paths):
            continue

        for file in files:
            file_path = os.path.join(root, file)

            if is_ignored_file(file_path, ignore_paths):
                continue

            content = read_file_safely(file_path)
            if content:
                parsed_docs.append({
                    "file_path": file_path,
                    "content": content
                })

    return parsed_docs


# Example usage
if __name__ == '__main__':
    from core.github_loader import get_repository
    repo = get_repository()
    docs = parse_repo(repo)
    print(f"Parsed {len(docs)} files.")
