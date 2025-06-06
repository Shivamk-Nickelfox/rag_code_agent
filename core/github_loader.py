# core/github_loader.py

import os
from dotenv import load_dotenv
load_dotenv()
import git
from core.utillls import load_config

CONFIG = load_config()


def load_local_repo_path():
    repo_url= CONFIG['github_repo']['url']
    if not os.path.exists(repo_url):
        raise FileNotFoundError(f"Local repository path '{repo_url}' does not exist.")
    return repo_url


def clone_remote_repo():
    repo_url_env = CONFIG['github_repo']['repo_url_env']
    repo_url = os.getenv(repo_url_env)
    local_dir = "./raw_repo"

    if os.path.exists(local_dir):
        print("Repository already cloned. Skipping...")
    else:
        print(f"Cloning from {repo_url} into {local_dir}...")
        git.Repo.clone_from(repo_url, local_dir)

    return local_dir


def get_repository():
    repo_type = CONFIG['github_repo']['type']

    if repo_type == 'local':
        return load_local_repo_path()
    elif repo_type == 'remote':
        return clone_remote_repo()
    else:
        raise ValueError(f"Unsupported repo type: {repo_type}")


# Example usage
if __name__ == '__main__':
    repo_path = get_repository()
    print(f"Loaded repo at: {repo_path}")
