import sys                      # For parsing input parameters
import multiprocessing as mp    # For sniffer daemon
import REST_API as rest         # For REST object
import time                     # Used to sleep in controller contact
import re                       # Regex to extract switch name from termination point
import packet_sniffer as ps     # To startup sniffer daemon
import random                   # For Demo

# Registry and decorator to add functions called with --args without explicitly coding them
# Improper number of arguments or no arguments must be errored within the function and caught by the try block at function call
registry = {}
def register(callstring):
    def funcRegister(func):
        registry[callstring] = func
        return func
    return funcRegister

# Basic driver class to add functionality and variables from flag calls
class driver():
    def __init__(self):
        self.verbose = False
        self.veryVerbose = False
        self.topology = {}
        self.flows = {}

    def readTopoInfo(self):
        """
        Provides a dictionary of the host topology where the key is the host ID, and the value is a dictionary of the MAC, IP, termination point, and switch ID
        """
        response = self.restModule.get_topo()[1]
        for node in response['network-topology']['topology'][0]['node']:
            if "host" in node['node-id']:
                self.topology[node['node-id']] = {'mac':node['host-tracker-service:addresses'][0]['mac'],
                                                'ip':node['host-tracker-service:addresses'][0]['ip'],
                                                'tp':node['host-tracker-service:attachment-points'][0]['tp-id'], 
                                                'tp-switch':re.sub(r'(?<=openflow:\d)\:\d*' , '', node['host-tracker-service:attachment-points'][0]['tp-id'])}

    def dropHost(self, switch, tableId, flowName, flowId, ethAddr, priority):
        """
        Pushes a flow to the controller to drop the selected host, returns true if the flow exists or is pushed and false otherwise
        """
        response = self.restModule.put_drop(switch, tableId, flowName, flowId, ethAddr, priority)
        if response.status_code == 201:
            self.flows[flowId] = {'switch': switch, 'tableId': tableId}
            return True
        elif response.status_code == 200:
            return True
        else:
            return False

@register("--SNIF")
def beginSniffing(arguments, controlObj):
    """
    Starts a daemon to sniff packets and places them in a queue for processing
    """
    controlObj.SNIF = arguments[0]
    if controlObj.verbose : print(f"Starting sniffer on iface {controlObj.SNIF}")
    controlObj.sniffer = mp.Process(target=ps.sniff_infinite, args=(controlObj.SNIF, controlObj.queue), daemon=True)
    controlObj.sniffer.start()


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
    for attempts in range(5):
        if controlObj.verbose : print(f"Attempt {attempts + 1}")
        try:
            response = controlObj.restModule.get_topo()[0]
        except:
            response = -1   
        if response == 200:
            contact = True
            break
        time.sleep(2)
    
    if controlObj.verbose and contact : print("Established contact with controller")
    if not contact : raise Exception("Controller is unreachable or does not have a topology")

if __name__ == "__main__":
    argumentGroups = {}
    argPrev = ""
    dataHolder = driver()
    dataHolder.queue = mp.Queue()

    # Parse the supplied flags and place them in a dictionary with their arguments
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
    
    # If no Controller IP or Sniffer IP are supplied throw an error, these are needed to continue
    if "--CTIP" not in argumentGroups:
        raise Exception("Controller IP must be specified with --CTIP [IP]")

    if "--SNIF" not in argumentGroups:
        raise Exception("Interface to sniff must be specified with --SNIF [IFACE]")
    
    if dataHolder.verbose : print(f"Beginning setup with args: {argumentGroups}")
    # Run through each flag's function
    for flag, params in argumentGroups.items():
        try:
            registry[flag](params, dataHolder)
        except KeyError as err:
            raise Exception(f"Flag \"{flag}\" is not implemented") from err
        except Exception as err:
            raise err
    
    if dataHolder.verbose : print("Setup complete, reading topology")
    # Now that we know the controller exists, poll and store the topology
    dataHolder.readTopoInfo()

    if dataHolder.verbose: 
        print(f"Topology information: {dataHolder.topology}")
        print("Beginning packet processing")
    
    ctr = 0
    keys = []
    while True:
        pkt = dataHolder.queue.get()
        if dataHolder.veryVerbose: print(pkt)

        # For demonstration purposes we will kill a random connection every 50 packets
        if ctr < 50:
            ctr += 1
        else:
            ctr = 0
            if dataHolder.verbose : print(f"Flows: {dataHolder.flows}")
            if dataHolder.flows:
                for key in dataHolder.flows:
                    resp = dataHolder.restModule.delete_flow(dataHolder.flows[key]['switch'], dataHolder.flows[key]['tableId'], key)
                    if resp == 200:
                        if dataHolder.verbose : print(f"Removed flow {key}")
                        keys.append(key)
                    else:
                        if dataHolder.verbose : print(f"Failed to remove flow {key}")
                for key in keys:
                    del dataHolder.flows[key]
                keys.clear()
            for key in dataHolder.topology:
                if random.randrange(0, 4) == 0:
                    dropped = dataHolder.dropHost(
                        dataHolder.topology[key]['tp-switch'],
                        0,
                        random.randrange(0, 100),
                        random.randrange(0, 100),
                        dataHolder.topology[key]['mac'],
                        random.randrange(0, 100)
                    )
                    if dropped:
                        if dataHolder.verbose : print(f"Blocking {key}")
        
