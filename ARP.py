import subprocess
import numpy as np
import pandas as pd
import os
from mac_vendor_lookup import MacLookup


def arp_network():
    output = subprocess.check_output(("arp", "-a"))
    just_data = output.split()[9:]
    tabularized = np.array(just_data).reshape(int(len(just_data)/3), 3)

    device_df = pd.DataFrame(tabularized, columns=["ip", "mac", "type"])

    for device_mac in device_df["mac"]:
        device_mac = str(device_mac)[2:-1].replace("-", "").upper()
        try:
            print(MacLookup().lookup(device_mac))
        except:
            print("NOT FOUND")



os.system('''cmd /c "netsh wlan connect name='1632 Front House-5G' interface=Wi-Fi"''')
arp_network()
os.system('''cmd /c "netsh wlan connect name='1632 Front House' interface=Wi-Fi"''')
arp_network()
