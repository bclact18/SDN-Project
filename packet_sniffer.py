import scapy.all as scapy                               # Allows for packet sniffing, manipulation, etc. 
#from sklearn.ensemble import RandomForestClassifier     # Used for supervised learning algo's 
import numpy as np                                      # Provides support for use of multi-dimensional arrays 

def sniff_packets(interface='eth0', count=100):
    print(f"Sniffing {count} packets on interface {interface}...")
    packets = scapy.sniff(iface=interface, count=count)
    return packets

#DO NOT CALL THIS OUTSIDE OF A CHILD PROCESS OR THREAD
#THIS WILL BLOCK EXECUTION
def sniff_infinite(interface, queue):
    """
    Sniffs for packets forever and places them into the queue
    """
    scapy.sniff(iface=interface, store=0, prn=lambda x : queue.put(x))

def extract_features(packets):
    features = []
    for packet in packets:
        # Extract relevant features from the packet
        # Example: source IP, destination IP, protocol, packet size, etc.
        # Here we are just using packet length as a feature
        features.append([len(packet)])
    return np.array(features)

def train_model(features, labels):
    print("Training Machine Learning model...")
    model = RandomForestClassifier()
    model.fit(features, labels)
    return model

def detect_anomalies(model, features):
    print("Detecting anomalies...")
    anomalies = model.predict(features)
    return anomalies

def main():
    # Assuming you have labeled data for training
    # For demonstration purposes, let's assume all packets are labeled as normal
    normal_labels = [0] * 100
    packets = sniff_packets()
    features = extract_features(packets)
    model = train_model(features, normal_labels)
    anomalies = detect_anomalies(model, features)
    
    # Print detected anomalies
    print("Detected anomalies:")
    for i, anomaly in enumerate(anomalies):
        if anomaly == 1:
            print(f"Packet {i+1}: Anomaly detected!")

if __name__ == "__main__":
    main()
