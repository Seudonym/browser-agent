from browser_agent import BrowserAgent


def main():
    agent = BrowserAgent()

    while True:
        command = input("> ")
        if command == "exit":
            break
        elif command.strip() == "":
            continue
        agent.execute_command(command)


if __name__ == "__main__":
    main()
