import requests

# Define the base URL of the REST API
base_url = "http://your_controller_api_base_url"

# Function to issue HTTP GET request
def get_request(endpoint):
    url = f"{base_url}/{endpoint}"
    response = requests.get(url)
    return response.json()

# Function to issue HTTP POST request
def post_request(endpoint, data):
    url = f"{base_url}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Function to issue HTTP PUT request
def put_request(endpoint, data):
    url = f"{base_url}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, json=data, headers=headers)
    return response.json()

# Function to issue HTTP DELETE request
def delete_request(endpoint):
    url = f"{base_url}/{endpoint}"
    response = requests.delete(url)
    return response.status_code

# Example usage
if __name__ == "__main__":
    # Example GET request
    response_data = get_request("some_endpoint")
    print("GET Response:", response_data)

    # Example POST request
    post_data = {"key": "value"}
    response_data = post_request("some_endpoint", post_data)
    print("POST Response:", response_data)

    # Example PUT request
    put_data = {"key": "new_value"}
    response_data = put_request("some_endpoint", put_data)
    print("PUT Response:", response_data)

    # Example DELETE request
    status_code = delete_request("some_endpoint")
    print("DELETE Status Code:", status_code)
