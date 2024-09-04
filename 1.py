import subprocess
import time
import threading
import signal
import os
import sys
import requests
from colorama import init, Fore, Style
from pystyle import *
from pystyle import Colors, Colorate

# Logo and credits
logo = """
  ____                                   _____      _     _    _       _     
 |  _ \\                                 / ____|    | |   | |  | |     | |    
 | |_) | __ _ _ __   __ _ _ __   __ _  | |     __ _| |_  | |__| |_   _| |__  
 |  _ < / _` | '_ \\ / _` | '_ \\ / _` | | |    / _` | __| |  __  | | | | '_ \\ 
 | |_) | (_| | | | | (_| | | | | (_| | | |___| (_| | |_  | |  | | |_| | |_) |
 |____/ \\__,_|_| |_|\\__,_|_| |_|\\__,_|  \\_____\\__,_|\\__| |_|  |_|\\__,_|_.__/ 
                                                                                                                                                                                                              
"""
credit = """
[+] Made by Dustin and Neyoshit
"""

credit2 = """
[+] discord.gg/chuoihub
          
          
"""

print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter(logo)))
print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter(credit)))
print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter(credit2)))

# Directories to manage
directories_delta = [
    "/storage/emulated/0/Android/data/com.roblox.client/files/delta/autoexec",
    "/storage/emulated/0/Android/data/com.roblox.clienu/files/delta/autoexec",
    "/storage/emulated/0/Android/data/com.roblox.clienv/files/delta/autoexec",
    # Add more directories if necessary
]

directories_fluxus = [
    "/storage/emulated/0/Android/data/com.roblox.client/files/fluxus/autoexec",
    "/storage/emulated/0/Android/data/com.roblox.clienu/files/fluxus/autoexec",
    # Add more directories if necessary
]

directories_codex = [
    "/storage/emulated/0/RobloxClone001/Codex/Autoexec/",
    "/storage/emulated/0/RobloxClone002/Codex/Autoexec/",
    # Add more directories if necessary
]

default_code = 'loadstring(game:HttpGet("https://raw.githubusercontent.com/mizuharasup/toolrejon/main/rejoin.lua"))()'

keys_needed = 0

# Auto-rejoin logic integrated from main.py
def join_game(package_name, private_server_link):
    time.sleep(20)
    force_stop_roblox(package_name, private_server_link)
    start_command = f"am start -n {package_name}/{package_name}.ActivityProtocolLaunch -d '{private_server_link}'"
    try:
        subprocess.run(start_command, shell=True, check=True)
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Started Roblox app: {package_name} with link: {private_server_link}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error starting Roblox: {str(e)}")

def force_stop_roblox(package_name, private_server_link):
    force_stop_command = f"am start -a android.intent.action.VIEW -d '{private_server_link}' {package_name}"
    try:
        subprocess.run(force_stop_command, shell=True, check=True)
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Restart Roblox app: {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error force-stopping Roblox app: {package_name}, {e}")

def notify_flask(package_name, private_server_link, id):
    url = 'http://localhost:5000/join'
    data = {
        'package_name': package_name,
        'private_server_link': private_server_link,
        'id': id
    }
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Failed to notify Flask server: {str(e)}")

def create_rejoin_check_file(directories):
    for directory in directories:
        rejoin_check_file = os.path.join(directory, "budaicho.txt")
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(rejoin_check_file):
                with open(rejoin_check_file, "w") as file:
                    file.write(default_code)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error creating file {rejoin_check_file}: {e}")

def save_user_input_to_autoexec(directories):
    user_choice = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Do you want to enter the code into autoexec.txt? (y/n): ")
    if user_choice.lower() == 'y':
        user_input = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Enter the script you want to save into autoexec.txt: ")
        for directory in directories:
            autoexec_file = os.path.join(directory, "autoexec.txt")
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(autoexec_file, "a") as file:
                    file.write(user_input + "\n")
                print(f"Saved code in {autoexec_file}")
            except Exception as e:
                print(f"Error saving code to file {autoexec_file}: {e}")

def auto_bypass_delta():
    def bypass_once():
        headers = {
            'Authorization': 'Bearer Neyoshi'
        }
        try:
            with open("usernames.txt", "r") as f:
                usernames = f.readlines()
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}[ ERROR ] >>{Fore.RESET} usernames.txt not found. Please create the file and add usernames.")
            return
        
        for username in usernames:
            username = username.strip()
            if username:
                try:
                    response = requests.get(f"https://sech.goatbypassers.xyz/?username={username}", headers=headers)
                    response.raise_for_status()
                    response_data = response.json()
                    key = response_data.get('key', 'No key')
                    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Processed {username}: {key} ({response.status_code})")
                except requests.RequestException as e:
                    print(f"{Fore.LIGHTRED_EX}[ ERROR ] >>{Fore.RESET} Error processing {username}: {e}")
                except ValueError:
                    print(f"{Fore.LIGHTRED_EX}[ ERROR ] >>{Fore.RESET} Error parsing JSON response for {username}")
    
    bypass_once()

def select_directory_type():
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Select directory type:")
    print(f"{Fore.LIGHTYELLOW_EX}[ 1 ] >>{Fore.RESET} Delta")
    print(f"{Fore.LIGHTYELLOW_EX}[ 2 ] >>{Fore.RESET} Fluxus")
    print(f"{Fore.LIGHTYELLOW_EX}[ 3 ] >>{Fore.RESET} Codex")
    choice = input(f"{Fore.LIGHTRED_EX}[ OPTION ] >>{Fore.RESET} Enter your choice (1, 2, or 3): ")

    if choice == '1':
        create_rejoin_check_file(directories_delta)
        save_user_input_to_autoexec(directories_delta)
        auto_bypass_choice = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Do you want to auto-bypass delta? (y/n): ")
        if auto_bypass_choice.lower() == 'y':
            create_usernames_file()
            auto_bypass_delta()
    elif choice == '2':
        create_rejoin_check_file(directories_fluxus)
        save_user_input_to_autoexec(directories_fluxus)
    elif choice == '3':
        create_rejoin_check_file(directories_codex)
        save_user_input_to_autoexec(directories_codex)
    else:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Invalid choice. Please select again.")
        select_directory_type()

def create_usernames_file():
    with open("usernames.txt", "w") as f:
        usernames = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Input usernames (e.g., account1 account2): ")
        for username in usernames.split():
            f.write(f"{username}\n")
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Usernames saved to usernames.txt")

def save_usernames_to_file(usernames):
    file_path = "/storage/emulated/0/usernames.txt"
    with open(file_path, 'a') as file:
        for username in usernames:
            file.write(username + "\n")
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Saved {len(usernames)} usernames")

def check_and_create_usernames_file():
    file_path = "/storage/emulated/0/usernames.txt"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass
    return file_path

def get_usernames_from_file():
    file_path = check_and_create_usernames_file()
    with open(file_path, 'r') as file:
        usernames = [line.strip() for line in file]
    return usernames

games = {
    "bloxFruits": "roblox://placeID=2753915549",
    "animeDefenders": "roblox://placeID=17017769292"
}

roblox_clients = [
    "com.roblox.clienu",
    "com.roblox.clienv",
    "com.roblox.clienw",
    "com.roblox.clienx",
    "com.roblox.clieny",
    "com.roblox.clienz",
    "com.roblox.clienp",
    "com.roblox.clienq",
    "com.roblox.clienr",
    "com.roblox.cliens"
]

special_client = "com.roblox.client"
selected_clients = []
selected_game_url = ""
stop_threads = threading.Event()
close_interval = 25

def signal_handler(sig, frame):
    stop_threads.set()
    cleanup()

signal.signal(signal.SIGINT, signal_handler)

def select_game():
    global selected_game_url, game_name
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Select a game to open:")
    print(f"{Fore.LIGHTYELLOW_EX}[ 1 ] >>{Fore.RESET} Blox Fruits")
    print(f"{Fore.LIGHTYELLOW_EX}[ 2 ] >>{Fore.RESET} Anime Defenders")
    print(f"{Fore.LIGHTYELLOW_EX}[ 3 ] >>{Fore.RESET} Enter another game ID")
    choice = input(f"{Fore.LIGHTRED_EX}[ OPTION ] >>{Fore.RESET} Enter your choice (1, 2, or 3): ")

    if choice == '1':
        selected_game_url = games['bloxFruits']
        game_name = "Blox Fruits"
    elif choice == '2':
        selected_game_url = games['animeDefenders']
        game_name = "Anime Defenders"
    elif choice == '3':
        game_id = input("Enter the game ID: ")
        game_name = input("Enter the game name: ")
        selected_game_url = f"roblox://placeID={game_id}"
    else:
        print("Invalid choice. Please select again.")
        select_game()

    add_server_choice = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET}Do you want to add a private server? (y/n): ")
    if add_server_choice.lower() == 'y':
        private_server_url = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET}Enter the full URL of the private server: ")
        save_url_to_file(game_name, private_server_url)
        selected_game_url = private_server_url
    else:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET}Using default URL: {selected_game_url}")

def select_client_type():
    global selected_client_type
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Select the client type to open:")
    print(f"{Fore.LIGHTYELLOW_EX}[ 1 ] >>{Fore.RESET} Special client (com.roblox.client)")
    print(f"{Fore.LIGHTYELLOW_EX}[ 2 ] >>{Fore.RESET} Other clients")
    client_type = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Enter your choice (1 or 2): ")

    if client_type == '1' or client_type == '2':
        selected_client_type = int(client_type)
    else:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Invalid choice. Please select again.")
        select_client_type()

def select_client_count():
    global selected_client_count
    if selected_client_type == 2:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Select the number of clients to open (1-10):")
        client_count = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Enter your choice: ")

        if client_count.isdigit() and 1 <= int(client_count) <= 10:
            selected_client_count = int(client_count)
            global selected_clients
            selected_clients = roblox_clients[:selected_client_count]
        else:
            print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Invalid choice. Please select again.")
            select_client_count()
    else:
        selected_client_count = 1
        selected_clients = [special_client]

def save_url_to_file(game_name, url):
    file_name = f"/storage/emulated/0/roblox_{game_name}_server_url.txt"
    with open(file_name, 'w') as file:
        file.write(url)
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} URL saved")

def set_close_interval():
    global close_interval
    close_interval_input = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Enter the interval to close clients (minutes): ")
    if close_interval_input.isdigit():
        close_interval = int(close_interval_input)
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Close interval set to {close_interval} minutes.")
    else:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Invalid choice. Using default value of 25 minutes.")
        close_interval = 25

def cleanup():
    print("Closing processes...")
    close_clients_immediate()
    sys.exit(0)

def close_clients_immediate():
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Closing clients immediately...")
    for client in selected_clients:
        result = subprocess.run(["pgrep", "-f", client], capture_output=True, text=True, universal_newlines=True)
        if result.stdout:
            client_pids = result.stdout.strip().split('\n')
            for client_pid in client_pids:
                try:
                    subprocess.run(["sudo", "kill", "-9", client_pid])
                    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Closed client: {client}")
                except subprocess.CalledProcessError as e:
                    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error closing client {client}: {e}")

def open_roblox(game_url, client_name):
    print(f"Checking existence of client: {client_name}...")
    result = subprocess.run(["pm", "list", "packages", client_name], capture_output=True, text=True, universal_newlines=True)
    if client_name in result.stdout:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Client {client_name} exists. Opening...")
        try:
            subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", game_url, "-p", client_name], check=True)
            print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Opened Roblox with URL: {game_url} using client: {client_name}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error opening Roblox with client {client_name}: {e}")
    else:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Client {client_name} does not exist.")

def is_client_in_game(client_name):
    try:
        result = subprocess.run(["logcat", "-d"], capture_output=True, text=True, universal_newlines=True, errors='ignore')
        log_output = result.stdout
        if client_name in log_output and "joined the game" in log_output:
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error checking game status for client {client_name}: {e}")
        return False

def monitor_clients():
    while not stop_threads.is_set():
        for client in selected_clients:
            if stop_threads.is_set():
                break
            print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Checking client {client}...")
            result = subprocess.run(["pgrep", "-f", client], capture_output=True, text=True, universal_newlines=True)
            if not result.stdout:
                print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Client {client} has been closed (process not found). Reopening...")
                open_roblox(selected_game_url, client)
                time.sleep(10)
            elif not is_client_in_game(client):
                print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Client {client} is not in game. Restarting...")
                open_roblox(selected_game_url, client)
                time.sleep(10)
            else:
                print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Client {client} is in game.")
                check_for_disconnect(client)
            time.sleep(2)
        time.sleep(5)

def check_for_disconnect(client):
    try:
        result = subprocess.run(["logcat", "-d"], capture_output=True, text=True, errors='ignore')
        log_output = result.stdout
        if any(code in log_output for code in ["Error Code: 278", "Error Code: 279"]):
            print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Client {client} encountered a disconnect issue (error code). Reopening...")
            open_roblox(selected_game_url, client)
            time.sleep(10)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error checking logcat for client {client}: {e}")

def close_clients():
    while not stop_threads.is_set():
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Closing selected clients...")
        for client in selected_clients:
            if stop_threads.is_set():
                break
            result = subprocess.run(["pgrep", "-f", client], capture_output=True, text=True, universal_newlines=True)
            if result.stdout:
                client_pids = result.stdout.strip().split('\n')
                for client_pid in client_pids:
                    try:
                        subprocess.run(["sudo", "kill", "-9", client_pid])
                        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Closed client: {client}")
                    except subprocess.CalledProcessError as e:
                        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Error closing client {client}: {e}")
            else:
                print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} No processes found for client: {client}")
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Waiting {close_interval} minutes before closing clients again...")
        time.sleep(close_interval * 60)

def input_usernames():
    num_usernames = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Enter the number of usernames to input (1-10): ")
    if num_usernames.isdigit() and 1 <= int(num_usernames) <= 10:
        usernames = []
        for _ in range(int(num_usernames)):
            username = input(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Enter username: ")
            usernames.append(username)
        save_usernames_to_file(usernames)
    else:
        print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Invalid choice. Please try again.")
        input_usernames()

# Workflow execution
select_game()

select_client_type()

select_client_count()

select_directory_type()

set_close_interval()

if selected_client_type == 1:
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Opening special client...")
    open_roblox(selected_game_url, special_client)
else:
    print(f"{Fore.LIGHTRED_EX}[ INFO ] >>{Fore.RESET} Opening {selected_client_count} other clients...")
    for client in selected_clients:
        open_roblox(selected_game_url, client)
        time.sleep(2)

client_monitor_thread = threading.Thread(target=monitor_clients)
client_close_thread = threading.Thread(target=close_clients)

client_monitor_thread.start()
client_close_thread.start()

try:
    client_monitor_thread.join()
    client_close_thread.join()
except KeyboardInterrupt:
    cleanup()
