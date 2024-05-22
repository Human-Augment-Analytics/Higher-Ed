import requests
import base64

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

def check_directory(path):
    # url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(url)
    files = response.json()

    if isinstance(files, list):
        for file in files:
            if file['type'] == 'file':
                file_url = file['url']
                file_response = requests.get(file_url)
                content = base64.b64decode(file_response.json()['content']).decode('utf-8')

                if marker in content:
                    print(f"The file {file['path']} is tested and finalized.")
                else:
                    print(f"The file {file['path']} is not tested and finalized.")
            elif file['type'] == 'dir':
                check_directory(file['path'])
    else:
        print(f"Error checking directory {path}: {files}")

check_directory(path)