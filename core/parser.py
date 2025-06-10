import os
from core.utillls import load_config
from core.utillls import is_ignored_file, read_file_safely

CONFIG = load_config()

ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.html', '.css', '.json', '.txt'}

def parse_repo(repo_path):
    parsed_docs = []
    ignore_paths = CONFIG.get('ignore_paths', [])

    for root, _, files in os.walk(repo_path):
        if any(ignored in root for ignored in ignore_paths):
            continue

        for file in files:
            file_path = os.path.join(root, file)

            # Skip ignored files or unsupported extensions
            ext = os.path.splitext(file)[-1].lower()
            if is_ignored_file(file_path, ignore_paths) or ext not in ALLOWED_EXTENSIONS:
                continue

            content = read_file_safely(file_path)
            if content.strip():
                parsed_docs.append({
                    "file_path": file_path,
                    "content": content
                })
            else:
                print(f"Skipped empty or unreadable file: {file_path}")

    print(f"✅ Parsed {len(parsed_docs)} valid documents from {repo_path}")
    return parsed_docs
