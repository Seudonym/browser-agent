from termcolor import colored

def log_info(message):
    print(colored(f"[-] {message}", "blue"))

def log_warning(message):
    print(colored(f"[!] {message}", "yellow"))

def log_error(message):
    print(colored(f"[x] {message}", "red"))

def log_success(message):
    print(colored(f"[] {message}", "green"))
