import socket
import threading
import os

# ------------------------------
# Function to scan a single port
# ------------------------------
def scan_port(target, port, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # quick timeout
        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()
                if not banner:
                    banner = "Service Detected (No Banner)"
            except:
                banner = "Unknown Service"
            
            message = f"[OPEN] Port {port} : {banner}"
            print(message)
            results.append(message)

        sock.close()
    except:
        pass


# ------------------------------
# Main scanner function
# ------------------------------
def port_scanner(target, start_port, end_port, filename):
    print(f"\n🔎 Scanning {target} on ports {start_port}-{end_port}...\n")

    results = []
    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, "w") as f:
        if results:
            for r in results:
                f.write(r + "\n")
        else:
            f.write("No open ports found.\n")

    print(f"\n✅ Scan complete. Results saved to {file_path}")


# ------------------------------
# Interactive Input
# ------------------------------
if __name__ == "__main__":
    target = input("Enter target (IP/Domain): ").strip()

    while True:
        try:
            start_port = int(input("Enter start port (e.g. 20): ").strip())
            end_port = int(input("Enter end port (e.g. 100): ").strip())
            if start_port < 0 or end_port > 65535 or start_port > end_port:
                print("⚠️ Invalid port range. Try again.")
                continue
            break
        except ValueError:
            print("⚠️ Please enter a valid number for ports.")

    filename = input("Enter output file name (default: results.txt): ").strip()
    if filename == "":
        filename = "results.txt"
    elif not filename.endswith(".txt"):
        filename += ".txt"

    port_scanner(target, start_port, end_port, filename)
