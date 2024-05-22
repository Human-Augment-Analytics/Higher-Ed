import requests
import base64
import time
import os

# Replace with your repo details and file path
owner = 'Human-Augment-Analytics'
repo = 'HAAG-Scripts-Repo'
path = r'Personal Folders/KaileyCozart/Week 2 Code Submission (05.24.24)/Automated Tag Reading'

# url_specific = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
# url = f'https://api.github.com/repos/{owner}/{repo}/contents'
# response = requests.get(url)
# files = response.json()

# Replace with your marker
marker = '# TESTED AND DOCUMENTED'

# Get the personal access token from the environment variable
token = os.getenv('GH_PAT')

headers = {
    'Authorization': f'token {token}',
}

def get(url):
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            retry_after = int(response.headers['Retry-After'])
            time.sleep(retry_after)
        else:
            return response

def check_directory(path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = get(url)
    files = response.json()

    if isinstance(files, list):
        for file in files:
            if file['type'] == 'file':
                file_url = file['url']
                file_response = get(file_url)
                content = base64.b64decode(file_response.json()['content']).decode('utf-8')

                if marker in content:
                    print(f"The file {file['path']} is tested and finalized.")
                else:
                    print(f"The file {file['path']} is not tested and finalized.")
            elif file['type'] == 'dir':
                check_directory(file['path'])
    else:
        print(f"Error checking directory {path}: {files['message']}")

check_directory(path)