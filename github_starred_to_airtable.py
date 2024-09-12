import requests
import os
import json
from pyairtable import Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub API endpoint for starred repositories
GITHUB_API_URL = "https://api.github.com/user/starred"

# Airtable configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# File to store the IDs of repositories we've already added
STATE_FILE = "added_repos.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_state(added_repos):
    with open(STATE_FILE, 'w') as f:
        json.dump(added_repos, f)

def get_github_starred_repos(token):
    headers = {"Authorization": f"token {token}"}
    repos = []
    page = 1
    while True:
        response = requests.get(f"{GITHUB_API_URL}?page={page}", headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API request failed with status code {response.status_code}")
        page_repos = response.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1
    return repos

def add_repos_to_airtable(repos, added_repos):
    airtable = Api(AIRTABLE_API_KEY)
    table = airtable.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
    
    for repo in repos:
        if repo['id'] not in added_repos:
            record = {
                'Name': repo['name'],
                'Description': repo['description'],
                'URL': repo['html_url'],
                'Language': repo['language']
            }
            table.create(record)
            added_repos.append(repo['id'])
            print(f"Added {repo['name']} to Airtable")
    
    return added_repos

def main():
    
    if not all([GITHUB_TOKEN, AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID]):
        print("Missing environment variables. Please check your .env file.")
        return
    
    try:
        added_repos = load_state()
        starred_repos = get_github_starred_repos(GITHUB_TOKEN)
        print(f"Found {len(starred_repos)} starred repositories.")
        
        updated_added_repos = add_repos_to_airtable(starred_repos, added_repos)
        save_state(updated_added_repos)
        
        print("Finished adding repositories to Airtable.")
        print(f"Total repositories processed: {len(updated_added_repos)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()