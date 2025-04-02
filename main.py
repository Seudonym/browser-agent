from browser_agent import BrowserAgent


def main():
    agent = BrowserAgent()

    while True:
        command = input(">>> ")
        if command == "exit":
            break
        agent.execute_command(command)


if __name__ == "__main__":
    main()
