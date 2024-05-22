import requests
import base64

# Replace with your repo details and file path
owner = 'Human-Augment-Analytics'
repo = 'HAAG-Scripts-Repo'
path = r'Personal Folders/KaileyCozart/Week 2 Code Submission (05.24.24)/Automated Tag Reading'

url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
response = requests.get(url)
files = response.json()
content = base64.b64decode(response.json()['content']).decode('utf-8')

# Replace with your marker
marker = '# TESTED AND DOCUMENTED'

for file in files:
    if file['type'] == 'file':
        file_url = file['url']
        file_response = requests.get(file_url)
        content = base64.b64decode(file_response.json()['content']).decode('utf-8')

        if marker in content:
            print(f"The file {file['path']} is tested and finalized.")
        else:
            print(f"The file {file['path']} is not tested and finalized.")