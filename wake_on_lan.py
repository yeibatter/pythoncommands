from wakeonlan import send_magic_packet
import time
import socket
import subprocess


def send_wake_on_lan1(mac_addr):
    print(f"\nEncendiendo: {mac_addr} ---")
    send_magic_packet(mac_addr)

# procesa el comando n veces
def send_wake_on_lan_times (mac_addr, times, sleep_time):
    for i in range(times):
        send_wake_on_lan1(mac_addr)
        send_wake_on_lan2(mac_addr)
        send_wake_on_lan3(mac_addr)
        time.sleep(sleep_time) 


def send_wake_on_lan2(mac_address: str):
    # Remove separators (colons or hyphens) and convert to lowercase
    cleaned_mac = mac_address.replace(':', '').replace('-', '').lower()
    
    if len(cleaned_mac) != 12:
        raise ValueError("Invalid MAC address format.")
    
    # Convert hex string to a bytes object (6 bytes)
    mac_bytes = bytes.fromhex(cleaned_mac)
    
    # Craft magic packet: 6 bytes of 0xFF followed by MAC address repeated 16 times
    magic_packet = b'\xFF' * 6 + mac_bytes * 16
    
    # Open a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Enable broadcasting status on the socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Broadcast packet to the network on port 9
        sock.sendto(magic_packet, ('255.255.255.255', 9))
        print(f"Magic packet sent to {mac_address}")

# Example usage (Replace with your target machine's actual MAC address)
# wake_on_lan('00:11:22:33:44:55')


def send_wake_on_lan3(mac_address: str):
    result = subprocess.run(['wakeonlan', mac_address], capture_output=True, text=True)

    # Access the results
    print("Exit Code:", result.returncode)
    print("Output:\n", result.stdout)
