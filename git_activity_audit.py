import os
import requests

# Configuration
GITHUB_ORG = "Innovexa-Hub"  # Replace with your exact GitHub organization name
GITHUB_TOKEN = os.getenv("GH_PAT_TOKEN")  # Set your Personal Access Token in environment variables

headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "vnd.github+json"}

def audit_team_repos():
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/repos?per_page=100"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch organization repositories: {response.status_code}")
        return

    repos = response.json()
    print(f"Auditing {len(repos)} team repositories in {GITHUB_ORG}...\n")
    
    for repo in repos:
        name = repo['name']
        if "team-" not in name.lower():
            continue  # Filter only team repositories
            
        commits_url = repo['commits_url'].replace("{/sha}", "")
        c_res = requests.get(commits_url, headers=headers)
        if c_res.status_code == 200:
            commits = c_res.json()
            print(f"[REPO: {name}] Total Commits: {len(commits)}")
            if len(commits) > 0:
                latest = commits[0]['commit']['committer']['date']
                print(f"  -> Last commit timestamp: {latest}")
            else:
                print(f"  -> WARNING: Zero commits found!")
        else:
            print(f"[REPO: {name}] No commit history accessible.")

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("ERROR: Please set your GH_PAT_TOKEN environment variable.")
    else:
        audit_team_repos()
