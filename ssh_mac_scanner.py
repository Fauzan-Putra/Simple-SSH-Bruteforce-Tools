from scapy.all import ARP, Ether, srp
import socket
import argparse

def arp_scan(ip_range):
    print(f"[INFO] Melakukan ARP scan di {ip_range}...")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=ip_range)
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]
    devices = []

    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def is_ssh_open(ip, port=22, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description="MAC Scanner & SSH Port Checker")
    parser.add_argument("--range", required=True, help="CIDR IP range (contoh: 192.168.1.0/24)")
    args = parser.parse_args()

    devices = arp_scan(args.range)
    print(f"[INFO] Ditemukan {len(devices)} perangkat aktif.\n")

    for device in devices:
        ip = device['ip']
        mac = device['mac']
        ssh_status = "OPEN" if is_ssh_open(ip) else "CLOSED"
        print(f"{ip:<15} {mac:<20} SSH: {ssh_status}")

if __name__ == "__main__":
    main()
