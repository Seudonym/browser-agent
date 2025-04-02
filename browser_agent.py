import json
from dotenv import load_dotenv
import os
from google import genai
from selenium import webdriver


class BrowserAgent:
    def __init__(self):
        load_dotenv()
        # TODO: Add more command types
        self.command_types = [
            "navigate",
            "click",
            "scroll",
            "search",
        ]

        self.function_decls = json.load(open("function_decls.json"))
        self.function_map = {
            "navigate": self.navigate,
            "click": self.click,
            "scroll": self.scroll,
            "search": self.search,
        }

        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # self.driver = webdriver.Chrome()

    def parse_command(self, command: str):
        response = self.client.models.generate_content(
            model="gemini-1.5-flash",  
            contents=[{
                "role": "user",
                "parts": [{
                    "text": f"""Based on this command: "{command}", which of these functions should be called: {', '.join(self.command_types)}?
                Return ONLY a JSON object with 'function' and 'params' keys. Make sure to use the description provided for each parameter to understand what to return. 
                For example, click should return the element's text which is to be clicked on. Make assumptions on the most probable text that is possible.
                Here are some examples of what you can return:""" +
                    """'Click on the login button' -> {{"function": "click", "params": {{"element": "login"}}}}
                'Navigate to google.com' -> {{"function": "navigate", "params": {{"url": "https://google.com"}}}}
                'Scroll to the bottom of the page' -> {{"function": "scroll", "params": {{"direction": "down"}}}}
                'Search for 'python'' -> {{"function": "search", "params": {{"query": "python"}}}}"""
                }]
            }],
            config={"temperature": 0.1}
        )

        response = response.candidates[0].content.parts[0].text
        try:
            response = response.replace("```json", "").replace("```", "")
            response = json.loads(response)
            function = response["function"]
            params = response["params"]
            print(function, params)
            return function, params
        except Exception as e:
            print(f"Error: {e}")
            return None, None

    def navigate(self, args):
        self.driver.get(url)

    def click(self, args):
        text = args["element"]
        pass

    def scroll(self, args):
        pass

    def search(self, args):
        pass
