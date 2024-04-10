import sys
import multiprocessing as mp
import REST_API as rest
import time
import re

# Registry and decorator to add functions called with --args without explicitly coding them
# Improper number of arguments or no arguments must be errored within the function and caught by the try block at function call
registry = {}
def register(callstring):
    def funcRegister(func):
        registry[callstring] = func
        return func
    return funcRegister

class driver():
    def __init__(self):
        self.verbose = False
        self.veryVerbose = False
        self.topology = {}

    def readTopoInfo(self):
        """
        Provides a dictionary of the host topology where the key is the host ID, and the value is a list with the MAC, IP, termination point, and switch ID
        """
        response = self.restModule.get_topo()[1]
        for node in response['network-topology']['topology'][0]['node']:
            if "host" in node['node-id']:
                self.topology[node['node-id']] = [re.sub(r'host\:', '', node['node-id']),
                                                node['host-tracker-service:addresses'][0]['ip'],
                                                node['host-tracker-service:attachment-points'][0]['tp-id'], 
                                                re.sub(r'(?<=openflow:\d)\:\d*' , '', node['host-tracker-service:attachment-points'][0]['tp-id'])]


@register("--SNIF")
def beginSniffing(arguments, controlObj):
    """
    TODO: Make sniffer work
    """
    if controlObj.verbose : print(f"Starting sniffer on iface {arguments[0]}") 
    controlObj.SNIF = arguments[0]

@register("--CTIP")
def getControllerContact(arguments, controlObj):
    """
    Constructs a RestFramework object for the control object, and then confirms that the controller is reachable and has a topology
    """
    if controlObj.verbose : print(f"Creating REST module for IP {arguments[0]}")
    controlObj.CTIP = arguments[0]
    controlObj.restModule = rest.RestFramework(controlObj.CTIP, 'admin', 'admin')
    if controlObj.verbose : print("Rest object created, attempting contact")
    contact = False
    if controlObj.restModule.get_topo()[0] != 200:
        for attempts in range(5):
            if controlObj.verbose : print(f"Attempt {attempts}")
            time.sleep(5)
            if controlObj.restModule.get_topo()[0] == 200:
                contact = True
                break
    else:
        if controlObj.verbose : print("Established contact with controller")
        contact = True
    if not contact:
        raise Exception("Controller is unreachable or does not have a topology")

if __name__ == "__main__":
    argumentGroups = {}
    argPrev = ""
    dataHolder = driver()

    #Parse the supplied flags and place them in a dictionary with their arguments
    for arg in sys.argv[1:]:
        if arg[0:2] == "--":
            if arg == "--v":
                dataHolder.verbose = True
            elif arg == "--vv":
                dataHolder.verbose = True
                dataHolder.veryVerbose = True
            else:
                argumentGroups[arg] = []
                argPrev = arg
        else:
            argumentGroups[argPrev].append(arg)
    
    #If no Controller IP or Sniffer IP are supplied throw an error, these are needed to continue
    if "--CTIP" not in argumentGroups:
        raise Exception("Controller IP must be specified with --CTIP [IP]")

    if "--SNIF" not in argumentGroups:
        raise Exception("Interface to sniff must be specified with --SNIF [IFACE]")
    
    if dataHolder.verbose : print(f"Beginning setup with args: {argumentGroups}")

    #Run through each flag's function
    for flag, params in argumentGroups.items():
        try:
            registry[flag](params, dataHolder)
        except KeyError as err:
            raise Exception(f"Flag \"{flag}\" is not implemented") from err
        except Exception as err:
            raise err
    
    if dataHolder.verbose : print("Setup complete, reading topology")

    dataHolder.readTopoInfo()

    if dataHolder.verbose : print(f"Topology information: {dataHolder.topology}")