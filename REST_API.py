import requests
import json

class RestFramework():
    def __init__(self, IP, user, passwd):
        if not IP:
            raise Exception("Controller IP is needed to begin")
        if not user or not passwd:
            raise Exception("Controller authentication not supplied")
        
        self.base_url = f"http://{IP}:8181"
        self.auth = (user, passwd)
        
        self.confEnd = '/restconf/config/'
        self.operEnd = '/restconf/operational/'
        self.topoEnd = self.operEnd + 'network-topology:network-topology/'
        self.nodeEnd = self.operEnd + 'opendaylight-inventory:nodes/'
        self.cnodeEnd = self.confEnd + 'opendaylight-inventory:nodes/'

    # Function to issue HTTP GET request
    def get_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers={'Accept': 'application/json'}, auth=self.auth, timeout=2)
        return response

    # Function to issue HTTP POST request
    def post_request(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers, auth=self.auth)
        return response

    # Function to issue HTTP PUT request
    def put_request(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.put(url, json=data, headers=headers, auth=self.auth)
        return response
    
    # Function to issue HTTP DELETE request
    def delete_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url)
        return response.status_code
    
    def get_topo(self):
        response = self.get_request(self.topoEnd)
        return [response.status_code, response.json()]

# Example usage
if __name__ == "__main__":
    testCont = RestFramework('192.168.56.106', 'admin', 'admin')
    print(testCont.get_topo())