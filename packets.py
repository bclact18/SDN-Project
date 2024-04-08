from scapy import all
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6

class packetReader:
    """
    Class to simplify packet handling.
    Takes in a whole raw packet or scapy ethernet frame and converts to a scapy ethernet frame if needed
    """
    def __init__(self, raw):
        if type(raw) is bytes:
            self.ethPacket = Ether(raw)
        elif type(raw) is Ether:
            self.ethPacket = raw
        else:
            raise Exception(f"packetReader only takes scapy Ethernet frames or bytes-like objects, received {type(raw)}")

    def isInitialized(self):
        if self.ethPacket: return True
        return False
    
    def getEthHeader(self):
        """
        Returns a list of ethernet header fields, or false if the frame is not ethernet
        """
        try:
            return [self.ethPacket[Ether].dst, self.ethPacket[Ether].src, self.ethPacket[Ether].type]
        except:
            return False
        
    def getARPHeader(self):
        """
        Returns a list of ARP header fields, or false if the frame is not ARP
        """
        try:
            return [self.ethPacket[ARP].hwtype, self.ethPacket[ARP].ptype,
                    self.ethPacket[ARP].hwlen, self.ethPacket[ARP].plen, self.ethPacket[ARP].op,
                    self.ethPacket[ARP].hwsrc, self.ethPacket[ARP].psrc,
                    self.ethPacket[ARP].hwdst, self.ethPacket[ARP].pdst]
        except:
            return False
    
    def getIPv4Header(self):
        """
        Returns a list of IPv4 headers in order, or false if the frame is not IPv4
        """
        try:
            return [self.ethPacket[IP].version, self.ethPacket[IP].ihl, self.ethPacket[IP].tos, self.ethPacket[IP].len, 
                self.ethPacket[IP].id, self.ethPacket[IP].flags, self.ethPacket[IP].frag, 
                self.ethPacket[IP].ttl, self.ethPacket[IP].proto, self.ethPacket[IP].chksum, 
                self.ethPacket[IP].src, self.ethPacket[IP].dst, self.ethPacket[IP].options]
        except:
            return False

    def getIPv6Header(self):
        """
        Returns a list of IPv6 headers in order, or false if the frame is not IPv4
        """
        try:
            return [self.ethPacket[IPv6].version, self.ethPacket[IPv6].tc, self.ethPacket[IPv6].fl, 
                self.ethPacket[IPv6].plen, self.ethPacket[IPv6].nh, self.ethPacket[IPv6].hlim, 
                self.ethPacket[IPv6].src, self.ethPacket[IPv6].dst]
        except:
            return False
    
    def getTCPHeader(self):
        """
        Returns a list of TCP headers in order, or false if the frame is not IPv4
        """
        try:
            return [self.ethPacket[TCP].sport, self.ethPacket[TCP].dport, 
                self.ethPacket[TCP].seq, self.ethPacket[TCP].ack, 
                self.ethPacket[TCP].dataofs, self.ethPacket[TCP].reserved, self.ethPacket[TCP].flags, self.ethPacket[TCP].window, 
                self.ethPacket[TCP].chksum, self.ethPacket[TCP].urgptr, 
                self.ethPacket[TCP].options]
        except:
            return False

    def getUDPHeader(self):
        """
        Returns a list of UDP headers in order, or false if the frame is not IPv4
        """
        try:
            return [self.ethPacket[UDP].sport, self.ethPacket[UDP].dport, 
                    self.ethPacket[UDP].len, self.ethPacket[UDP].chksum]
        except:
            return False
        
    def getRawPacket(self):
        return all.raw(self.ethPacket)
    
    def getScapyFrame(self):
        return self.ethPacket