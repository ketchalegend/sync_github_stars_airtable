# GitHub Starred Repos to Airtable Sync

This Python script allows you to sync your starred GitHub repositories to an Airtable table. It uses the GitHub API to fetch your starred repositories and then adds them to a specified Airtable base and table. The script also keeps track of repositories that have already been added to Airtable, ensuring no duplicates are added.

## Features
- Fetches starred repositories from your GitHub account.
- Adds repository details (name, description, URL, and language) to Airtable.
- Tracks which repositories have already been added using a local `added_repos.json` file.

## Prerequisites
1. **Python 3.x** installed on your machine.
2. A **GitHub Token** with access to starred repositories.
3. An **Airtable API key** and a configured Airtable base/table.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ketchalegend/sync_github_stars_airtable.git
cd github-starred-airtable-sync
```

### 2. Install dependencies

This script requires a few Python libraries to run. Install them using pip:

````
pip install requests pyairtable python-dotenv
````

### 3. Set up environment variables

Create a `.env` file in the root of the project with the following variables:

````
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_ID=your_airtable_table_id
GITHUB_TOKEN=your_github_token
````

* AIRTABLE_API_KEY: Your Airtable API key. You can generate this from your Airtable account.
* AIRTABLE_BASE_ID: The ID of the Airtable base where you want to add the repositories. You can find this in the URL when you open your base in Airtable.
* AIRTABLE_TABLE_ID: The ID of the table inside the base where the repositories should be added. This is usually the table name.
* GITHUB_TOKEN: Your GitHub personal access token with repo scope to read starred repositories. You can generate one from your GitHub Developer Settings.

### 4. Run the script

Once everything is set up, you can run the script using:

`````
python github_starred_to_airtable.py
`````

This script will:

- Fetch all starred repositories from your GitHub account.
- Add the repository details (name, description, URL, and language) to Airtable.
- Update the added_repos.json file to keep track of the repositories already added.

## Script Details

### Environment Variables

The script uses the following environment variables, which should be defined in your `.env` file:

- `AIRTABLE_API_KEY`: The API key to authenticate with Airtable.
- `AIRTABLE_BASE_ID`: The ID of the Airtable base.
- `AIRTABLE_TABLE_ID`: The name or ID of the Airtable table.
- `GITHUB_TOKEN`: The personal access token for accessing GitHub's API.

### State File

The script uses a file named `added_repos.json` to store the IDs of the repositories that have already been added to Airtable. This prevents adding the same repositories multiple times.

### GitHub API Rate Limits

The script makes multiple requests to GitHub's API, so keep in mind GitHub's rate-limiting policies. If you hit the limit, the script will stop and you will have to wait for the limit to reset.

### Error Handling

The script includes basic error handling. If there is an error with the GitHub API or Airtable, the script will output the error message and exit. The script retries failed GitHub API requests up to 5 times with exponential backoff.

### Example Output

When you run the script, it will print the following:

````
[+] Starting script
Found 25 starred repositories.
 ├ Scraping: https://github.com/username/repository-name
Added repository-name to Airtable
...
Finished adding repositories to Airtable.
Total repositories processed: 25
````

### License

This project is licensed under the MIT License. Feel free to use it as you see fit.




