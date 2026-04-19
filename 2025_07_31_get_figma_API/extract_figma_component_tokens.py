import requests
import json

TOKEN = 'YOUR_FIGMA_TOKEN'
headers = {
    "X-Figma-Token": TOKEN
}

file_key = "6dCATf55Qdby8cP0NfcY6n"
node_id = "1-5055"

url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
resp = requests.get(url, headers=headers)

data = resp.json()
with open('extract_figma_component_tokens.json', 'w') as f:
    json.dump(data, f, indent=2)
