import os
import json

HISTORY_PATH = 'Data/History/history.json'

def save_history(repo_url=None,prompt=None):
    """Save the history to a JSON file."""
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    history = load_history()
    if repo_url and repo_url not in history["repos"]:
        history["repos"].append(repo_url)
        if prompt and prompt not in history["prompts"]:
            history["prompts"].append(prompt)

    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)


def load_history():
    if os.path.exists(HISTORY_PATH):
        try:    
            with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure the structure is as expected
                if isinstance(data, dict):
                    repos = data.get("repos", [])
                    prompts = data.get("prompts", [])
                    return {
                        "repos": repos if isinstance(repos, list) else [],
                        "prompts": prompts if isinstance(prompts, list) else []
                    }

        except (json.JSONDecodeError, IOError):
            pass  # If file is corrupted or unreadable, fall back to default

    # Default empty history
    return {
        "repos": [],
        "prompts": []
    }
