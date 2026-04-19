# extract_figma_tokens.py
import requests
import json

# https://www.figma.com/design/6dCATf55Qdby8cP0NfcY6n/Demo?node-id=0-1&p=f&t=Cnsoit0FN3z4cEVl-0
TOKEN = 'YOUR_FIGMA_TOKEN'
FILE_KEY = '6dCATf55Qdby8cP0NfcY6n'

headers = {
    'X-Figma-Token': TOKEN
}

resp = requests.get(
    f'https://api.figma.com/v1/files/{FILE_KEY}', headers=headers)
data = resp.json()

# TODO: Parse node tree to extract specific component info
# You can start from data['document']['children']...

with open('figma_design.json', 'w') as f:
    json.dump(data, f, indent=2)
