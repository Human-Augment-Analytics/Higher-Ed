import csv
from datetime import datetime
from pathlib import Path
import requests
import shutil

with open('Bree Posts - Sheet1.csv', 'r', encoding='utf8') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

for i in data:
    pid = i['Post ID'].split(':')[-1]
    milli = int(bin(int(pid)).replace('0b', '')[:41], 2)
    date = datetime.fromtimestamp(milli/1000).strftime('%Y-%m-%d')
    pid = i['Post ID'].split(':')[-1]
    folder_name = f'{date}_{pid}'
    path = Path('posts') / Path(folder_name)
    path.mkdir(exist_ok=True, parents=True)
    with open(str(path / 'content.txt'), 'w', encoding='utf8') as outfile:
        outfile.write(i['Content'])
        outfile.write('\n\n')
        outfile.write(f'Post Link: {i['Post Link']}')
    if i['Image1']:
        r = requests.get(i['Image1'], stream=True)
        if r.status_code == 200:
            with open(str(path / 'image1.jpg'), 'wb') as outfile:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, outfile)
    if i['Image2']:
        r = requests.get(i['Image2'], stream=True)
        if r.status_code == 200:
            with open(str(path / 'image2.jpg'), 'wb') as outfile:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, outfile)
