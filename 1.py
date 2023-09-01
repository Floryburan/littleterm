import psutil

def list_network_interfaces():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        print(f"Interface: {interface}")
        for addr in addrs:
            print(f"  - {addr.family.name}: {addr.address}")

list_network_interfaces()
