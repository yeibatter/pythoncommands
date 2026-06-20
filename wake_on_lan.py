from wakeonlan import send_magic_packet
import time

def send_wake_on_lan(mac_addr):
    print(f"\n--- encendiendo: {mac_addr} ---")
    send_magic_packet(mac_addr)

# procesa el comando n veces
def send_wake_on_lan_times (mac_addr, times, sleep_time):
    for i in range(times):
        send_wake_on_lan(mac_addr)
        time.sleep(sleep_time) 