import requests
import base64

# Replace with your repo details and file path
owner = 'Human-Augment-Analytics'
repo = 'HAAG-Scripts-Repo'
path = 'Personal Folders/KaileyCozart/Week 2 Code Submission (05.24.24)/Automated Tag Reading'

url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
response = requests.get(url)
content = base64.b64decode(response.json()['content']).decode('utf-8')

# Replace with your marker
marker = '# TESTED AND DOCUMENTED'

if marker in content:
    print(f'The file {path} is tested and finalized.')
else:
    print(f'The file {path} is not tested and finalized.')