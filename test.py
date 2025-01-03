import requests

# Step 1: Login and save cookies
login_url = "LOGIN_URL"  # Replace with the login endpoint
api_url = "API_URL"      # Replace with the API endpoint

# Login payload
payload = {
    "username": "sysadmin",   # Replace with the username
    "password": "YOUR_PASSWORD",  # Replace with the password
    "domain": "Control Room"  # Replace with the domain if needed
}

# Start a session
session = requests.Session()

# Send login request
login_response = session.post(login_url, data=payload)

# Check if login is successful
if login_response.status_code == 200:
    print("Login successful!")
else:
    print("Login failed:", login_response.text)
    exit()

# Step 2: Fetch data using saved cookies
response = session.get(api_url)

if response.status_code == 200:
    print("Data fetched successfully!")
    print(response.json())  # or response.text, depending on the API response format
else:
    print("Failed to fetch data:", response.text)