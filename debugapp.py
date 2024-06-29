import requests

# Define the API endpoint
# api_url = 'http://127.0.0.1:5000/protected'
api_url = 'http://localhost:5000/protected'

print("Making GET request...")
response = requests.get(api_url)
if response.status_code == 200:
        print("GET request successful!")
        print("Response:", response.json())
else:
    print("GET request failed with status code:", response.status_code)
