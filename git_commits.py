import subprocess
from datetime import datetime
 
def get_git_commits_today():
    today = datetime.now().strftime("%Y-%m-%d")
    git_command = [
        "git",
        "log",
        f'--since={today} 00:00',
        f'--until={today} 23:59',
        '--pretty=format:%h - %an: %s'
    ]
 
    try:
        result = subprocess.run(git_command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if output:
            print(f"✅ Git commits for {today}:\n")
            print(output)
        else:
            print(f"ℹ️ No commits found for {today}.")
    except subprocess.CalledProcessError as e:
        print("❌ Error running git command:", e)
 
if __name__ == "__main__":
    get_git_commits_today()