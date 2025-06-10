# core/github_loader.py

import os
from dotenv import load_dotenv
load_dotenv()
import git
from core.utillls import load_config
import hashlib

CONFIG = load_config()



import os
import git
from core.utillls import load_config
from urllib.parse import urlparse

CONFIG = load_config()

def clone_remote_repo(raw_url=None):
    raw_url = os.getenv("DYNAMIC_GITHUB_URL") or CONFIG['github_repo']['url']
    token = os.getenv("GITHUB_TOKEN")
    is_private = os.getenv("GITHUB_PRIVATE_REPO", "false").lower() == "true"

    if not raw_url:
        raise ValueError("GitHub repository URL is not provided.")
    
    parsed = urlparse(raw_url)
    
    if is_private:
        if not token:
            raise ValueError("GitHub token is required for private repositories.")
        token_url = f"https://{token}@{parsed.hostname}{parsed.path}"

    else:
        token_url = raw_url
        print("Cloning public repository without token...")
    
    repo_hash = hashlib.md5(raw_url.encode()).hexdigest()

    local_dir = f"./data/repos/{repo_hash}"

    if os.path.exists(local_dir):
        print("Repository already cloned. Skipping...")
    else:
        print(f"Cloning from {token_url} into {local_dir}...")
        git.Repo.clone_from(token_url, local_dir)

    return local_dir

def get_repository():
    repo_type = CONFIG['github_repo']['type']
    if repo_type == 'remote':
        return clone_remote_repo()
    else:
        raise ValueError(f"Unsupported repo type: {repo_type}")



# Example usage
if __name__ == '__main__':
    repo_path = get_repository()
    print(f"Loaded repo at: {repo_path}")
