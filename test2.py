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

try:
    # Send login request
    login_response = session.post(login_url, data=payload)
    login_response.raise_for_status()  # Raise an error for bad status codes

    # Check if login is successful
    if login_response.status_code == 200:
        print("Login successful!")
    else:
        print("Login failed:", login_response.text)
        exit()

    # Step 2: Fetch data using saved cookies
    response = session.get(api_url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Check the Content-Type to determine how to process the response
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        data = response.json()
        print("Data fetched successfully!")
        print(data)
    else:
        print("Unexpected content type:", content_type)
        print("Response content:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)