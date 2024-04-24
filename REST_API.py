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
        response = requests.delete(url, auth=self.auth)
        return response.status_code
    
    def get_topo(self):
        response = self.get_request(self.topoEnd)
        return [response.status_code, response.json()]
    
    def put_drop(self, switch, tableId, flowName, flowId, ethAddr, priority):
        data = self.make_drop_request(tableId, flowName, flowId, ethAddr, priority)
        return self.put_request(f"{self.cnodeEnd}node/{switch}/table/{tableId}/flow/{flowId}", data)

    def delete_flow(self, switch, tableId, flowId):
        return self.delete_request(f"{self.cnodeEnd}node/{switch}/table/{tableId}/flow/{flowId}")

    def make_drop_request(self, tableId, flowName, flowId, ethAddr, priority):
        return {'flow':{
                'strict': 'true',
                'instructions':{
                    "instruction": {
                    "order": "0",
                    "apply-actions": {
                        "action": {
                            "order": "0",
                            "drop-action": {}
                            }
                        }
                    }
                },
                "table_id": tableId,
                "id": flowId,
                "cookie_mask": "0",
                "match": {
                    "ethernet-match": {
                        "ethernet-source": {
                            "address": ethAddr
                        }
                    }
                },
                "hard-timeout": "300",
                "cookie": "1234",
                "idle-timeout": "600",
                "flow-name": flowName,
                "priority": priority
            }}


# Example usage
if __name__ == "__main__":
    testCont = RestFramework('172.17.42.205', 'admin', 'admin')
    #print(testCont.get_topo())

    print(True if testCont.put_drop('openflow:1', '0', 'test', '1212', '00:00:00:00:00:01', '20').status_code == 201 else False)
    print(testCont.delete_flow('openflow:1', '0', '1212'))