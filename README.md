
# Browser Automation Agent

A **Browser Automation Agent** that allows users to interact with web browsers using natural language commands. The agent leverages the **MCP protocol**, **Gemini AI**, and **Selenium WebDriver** to interpret commands, map them to browser actions, and execute them seamlessly.

## Features

- **Natural Language Commands**: Accepts user input like "Navigate to google.com and search for 'Rust programming'" and executes it in the browser.
- **Automated Browser Actions**:
  - Navigate to URLs.
  - Click on elements (e.g., buttons, links).
  - Scroll up/down the page.
  - Search for queries on websites.
  - Type text into input fields.
- **AI-Powered Parsing**: Uses Gemini AI to convert natural language commands into structured JSON-RPC requests.
- **Dynamic Element Detection**: Locates elements dynamically using text or attributes.

---

## How It Works

1. **User Input**: The user provides a natural language command (e.g., "Go to YouTube and search for 'Python tutorials'").
2. **Command Parsing**:
   - The input is sent to Gemini AI, which parses it into structured commands with functions and parameters.
   - Example Output:
     ```
     [
       { "function": "navigate", "params": { "url": "https://www.youtube.com" } },
       { "function": "search", "params": { "query": "Python tutorials" } }
     ]
     ```
3. **Command Execution**:
   - The parsed commands are executed using Selenium WebDriver.
   - Each function (e.g., `navigate`, `click`, `scroll`) performs the corresponding browser action.

---

## Installation

### Prerequisites
- Python3 and uv
- Google Chrome installed
- ChromeDriver installed (compatible with your Chrome version)
- [Gemini API key](https://example.com) for AI command parsing

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/your-repo/browser-agent.git
   cd browser-agent
   ```

2. Install dependencies:
   ```
   uv sync
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

---

## Usage

1. Start the agent by running:
   ```
   uv run main.py
   ```

2. Enter natural language commands in the terminal, such as:
   - `Navigate to youtube.com`
   - `Search for 'Python tutorials'`
   - `Scroll down`
   - `Go to github and click on the login button`

3. To exit, type:
   ```
   exit
   ```

---

## Example Commands

| Command                              | Action                                                                 |
|--------------------------------------|------------------------------------------------------------------------|
| `Navigate to github.com`             | Opens GitHub in the browser.                                           |
| `Search for 'AI tools' on YouTube`    | Navigates to YouTube and searches for "AI tools".                       |
| `Scroll to the bottom of the page`   | Scrolls to the bottom of the current page.                             |
| `Click on the login button`          | Finds and clicks on a button with text containing "login".             |
| `Type 'hello' into the username field` | Types "hello" into an input field labeled or named "username".         |

---

## Project Structure

```
.
├── browser_agent.py        # Core logic for parsing and executing commands
├── function_decls.json     # Schema of supported functions and their parameters
├── logging_utils.py        # Utility functions for logging actions and errors
├── main.py                 # Entry point for running the agent
├── .env                    # Environment variables (e.g., Gemini API key)
└── README.md               # Project documentation (this file)
```

---

## Supported Commands

### 1. Navigate (`navigate`)
- **Description**: Opens a specified URL in the browser.
- **Parameters**:
  - `url` (string): The URL to navigate to.

### 2. Click (`click`)
- **Description**: Clicks on an element in the browser.
- **Parameters**:
  - `element` (string): Text or keyword from the element's content.

### 3. Scroll (`scroll`)
- **Description**: Scrolls up, down, left, or right on a webpage.
- **Parameters**:
  - `direction` (string): `"up"`, `"down"`, `"left"`, or `"right"`.
  - `bound` (boolean): Whether to scroll modestly (`false`) or all the way (`true`).

### 4. Search (`search`)
- **Description**: Searches for a query on a website.
- **Parameters**:
  - `query` (string): The search term.

### 5. Type (`type`)
- **Description**: Types text into an input field.
- **Parameters**:
  - `field` (string): Text or keyword identifying the field.
  - `text` (string): The text to type.

---

## Future Enhancements

1. Add support for more complex workflows, such as form submissions or multi-step tasks.
2. Improve element detection using fuzzy matching or AI-based visual recognition.
3. Integrate additional browsers like Firefox or Edge.
4. Provide a web-based interface for easier use.

---

