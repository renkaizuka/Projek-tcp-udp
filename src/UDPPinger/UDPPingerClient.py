# UDPPingerClient.py
from socket import *
import time

# Server host/port: change serverName to the IP address or hostname
# of the machine running UDPPingerServer.py when testing across hosts.
serverName = '10.177.162.177'
serverPort = 12000

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Wait up to one second for a reply before assuming the packet was lost
clientSocket.settimeout(1)

rtts = []

for sequence_number in range(1, 11):
    sendTime = time.time()
    message = f"Ping {sequence_number} {sendTime}"

    try:
        # (1) Send the ping message using UDP
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # (2) Print the response message from the server, if any
        response, serverAddress = clientSocket.recvfrom(1024)
        recvTime = time.time()

        # (3) Calculate and print the RTT, in seconds, of this packet
        rtt = recvTime - sendTime
        rtts.append(rtt)
        print(f"Reply from {serverName}: {response.decode()}   RTT: {rtt:.6f} sec")

    except timeout:
        # (4) Otherwise, print "Request timed out"
        print(f"Ping {sequence_number}: Request timed out")

clientSocket.close()

# --- Optional exercise 1: min/max/avg RTT and packet loss rate ---
sent = 10
received = len(rtts)
lost = sent - received
loss_rate = (lost / sent) * 100

print("\n--- Ping statistics ---")
print(f"Packets: Sent = {sent}, Received = {received}, Lost = {lost} ({loss_rate:.0f}% loss)")
if rtts:
    print(f"RTT: Min = {min(rtts):.6f}s, Max = {max(rtts):.6f}s, Avg = {sum(rtts) / len(rtts):.6f}s")
