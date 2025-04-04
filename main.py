from browser_agent import BrowserAgent
from logging_utils import log_info, log_success, log_error


def main():
    agent = BrowserAgent()

    while True:
        command = input("> ")
        if command == "exit":
            break
        elif command.strip() == "":
            continue
        try:
            agent.execute_command(command)
        except Exception as e:
            log_error(f"Error executing command: {e}")


if __name__ == "__main__":
    main()
