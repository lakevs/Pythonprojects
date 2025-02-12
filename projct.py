import socket
import threading
import queue
import sys
import time

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

open_ports = []
total_ports = 0
scanned_ports = 0

f = queue.Queue()

def banner():
    """Display an introductory banner"""
    print(f"""{GREEN}
    ##########################
    #     Advanced Port      #
    #      Scanner           #
    ##########################
    {RESET}
    """)

def scan_port(host, port):
    global scanned_ports
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        scanned_ports += 1
        if result == 0:
            print(f"{GREEN}Port {port} is OPEN{RESET}")
            open_ports.append(port)
        else:
            print(f"{RED}Port {port} is CLOSED{RESET}")
    except socket.error as e:
        print(f"{RED}Error with port {port}: {e}{RESET}")
    finally:
        sock.close()

def threader(host):
    while not f.empty():
        port = f.get()
        scan_port(host, port)
        f.task_done()

def scan_ports(host, ports):
    global total_ports
    total_ports = len(ports)
    
    print(f"{GREEN}Scanning {host} on {total_ports} ports...{RESET}")
    for port in ports:
        f.put(port)
    
    # Spawn threads for concurrent scanning
    for _ in range(50):  # You can adjust the number of threads
        t = threading.Thread(target=threader, args=(host,))
        t.daemon = True
        t.start()
    
    f.join()

def main():
    banner()

    host = input(f"Enter the target host (e.g., 192.168.1.1): ")

    ports_input = input(f"Enter the ports to scan (comma separated or range e.g., 20,80-100): ")
    
    ports = []
    for part in ports_input.split(","):
        if "-" in part:  
            start, end = part.split("-")
            ports.extend(range(int(start), int(end)+1))
        else:
            ports.append(int(part))

    start_time = time.time()
    scan_ports(host, ports)
    end_time = time.time()
    
    print(f"\nScan completed in {end_time - start_time:.2f} seconds.")
    print(f"Total ports scanned: {scanned_ports}")
    print(f"Open ports: {len(open_ports)}")
    
    if open_ports:
        print(f"{GREEN}Open ports: {open_ports}{RESET}")
    else:
        print(f"{RED}No open ports found.{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Scan interrupted by the user{RESET}")
        sys.exit(1)
