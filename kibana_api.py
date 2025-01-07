import requests
import json

# Configuration
KIBANA_URL = "http://<KIBANA_URL>"  # Replace with your Kibana URL
SEARCH_ENDPOINT = "/api/console/proxy?path=_search&method=POST"
BEARER_TOKEN = "<YOUR_BEARER_TOKEN>"  # Replace with your Bearer token
OUTPUT_JSON_FILE = "response.json"
INDEX_PATTERN = "filebeat-*"  # Replace with your index pattern
POD_NAME = "<POD_NAME>"  # Replace with your target pod name

# Headers with Bearer Token
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
    "kbn-xsrf": "true"  # Required for Kibana API
}

# Query Payload
search_payload = {
    "index": INDEX_PATTERN,
    "query": {
        "bool": {
            "must": [
                {"match": {"kubernetes.pod.name": POD_NAME}},
                {"range": {"@timestamp": {"gte": "now-1h", "lte": "now"}}}
            ]
        }
    }
}

try:
    # Send the API request
    response = requests.post(f"{KIBANA_URL}{SEARCH_ENDPOINT}", headers=headers, json=search_payload)
    response.raise_for_status()  # Raise an error for bad HTTP status codes

    # Save the response as a JSON file
    with open(OUTPUT_JSON_FILE, "w") as json_file:
        json.dump(response.json(), json_file, indent=4)

    print(f"Response saved to {OUTPUT_JSON_FILE}.")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
