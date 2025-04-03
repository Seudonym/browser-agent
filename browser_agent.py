import json
from dotenv import load_dotenv
import os
from time import sleep
from logging_utils import *

from google import genai
from selenium import webdriver
from selenium.webdriver.common.by import By


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
        self.driver = webdriver.Chrome()

        log_info("BrowserAgent initialized")

    def parse_command(self, command: str):
        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[{
                "role": "user",
                "parts": [{
                    "text": f"""Based on this command: "{command}", which of these functions should be called: {', '.join(self.command_types)}?
                Return ONLY an array of JSON objects with 'function' and 'params' keys. Make sure to use the description provided for each parameter to understand what to return.
                For example, click should return the element's text which is to be clicked on. Make assumptions on the most probable text that is possible.
                Here are some examples of what you can return:""" +
                    """'Click on the login button' -> {[{"function": "click", "params": {{"element": "login"}}}]}
                'Navigate to google.com' -> {[{"function": "navigate", "params": {{"url": "https://google.com"}}}]}
                'Scroll to the bottom of the page' -> {[{"function": "scroll", "params": {{"direction": "down", "bound": true}}}]}
                'Scroll down' -> {[{"function": "scroll", "params": {{"direction": "down", "bound": false}}}]}
                'Go to google.com and search for 'python'' -> {[{"function": "navigate", "params": {{"url": "https://google.com"}}}, {"function": "search", "params": {{"query": "python"}}}]}"""
                }]
            }],
            config={"temperature": 0.5}
        )

        response = response.candidates[0].content.parts[0].text
        try:
            response = response.replace("```json", "").replace("```", "")
            response = json.loads(response)
            log_success("Command parsed successfully")
            log_info(response)
            return response
        except Exception as e:
            log_error(f"{e}")
            return None

    def execute_command(self, command: str):
        parsed = self.parse_command(command)
        if parsed is None:
            raise Exception("Failed to parse command")

        for command in parsed:
            function, params = command["function"], command["params"]
            if function in self.command_types:
                log_info(
                    f"Executing command: {function} => {params}")
                self.function_map[function](params)
                self._sleep_till_page_load()
            else:
                raise Exception(f"Unknown command: {function}")

    def navigate(self, params):
        url = params["url"]
        self.driver.get(url)
        log_success("Navigated to " + url)

    def click(self, params):
        text = params["element"]
        button = self._find_button_by_text(text)
        button.click()
        log_success("Clicked on " + text)

    def scroll(self, params):
        direction = params["direction"]
        bound = params["bound"]
        scroll_amount = self._calc_scroll_amount(direction, bound)
        for _ in range(100):
            self.driver.execute_script(
                f"window.scrollBy(0, {scroll_amount // 100})")

    def search(self, params):
        search_bar = self._find_search_bar()
        search_bar.click()
        search_bar.send_keys(params["query"])
        search_bar.submit()

    # Helper functions
    # =====================
    def _calc_scroll_amount(self, direction, bound):
        if bound:
            scroll_amount = int(self.driver.execute_script(
                "return document.body.scrollHeight"))
        else:
            scroll_amount = int(self.driver.execute_script(
                "return window.innerHeight"
            )) // 1.1

        if direction == "up":
            scroll_amount = -scroll_amount

        return scroll_amount

    # WARNING: Fuzzy search is not being used anywhere yet. So remember to implement it
    def _find_button_by_text(self, text: str, fuzzy: bool = True):
        log_info(f"Finding button with text: {text}")

        def filter_func(x):
            extracted_text = x.text
            if extracted_text.strip() == "":
                extracted_text = x.get_attribute("value") or ""
            if fuzzy:
                return text.lower() in extracted_text.lower()
            else:
                return text == extracted_text

        anchors = self.driver.find_elements(By.TAG_NAME, "a")
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        buttons = self.driver.find_elements(By.TAG_NAME, "button")

        candidates = anchors + inputs + buttons
        candidates = filter(filter_func, candidates)
        candidates = list(candidates)
        log_info(f"Found {len(candidates)} candidates")
        if len(candidates) == 0:
            raise Exception("Element not found")
        else:
            return candidates[0]

    def _find_search_bar(self):
        search_bars = self.driver.find_elements(By.TAG_NAME, "input")
        search_bars = list(filter(lambda x: x.get_attribute(
            "type") == "text", search_bars))

        search_bars = search_bars + \
            self.driver.find_elements(By.TAG_NAME, "textarea")
        search_bars = list(filter(
            lambda x: "search" in x.accessible_name.lower(), search_bars))

        log_info(f"Found {len(search_bars)} search bars")
        if len(search_bars) == 0:
            raise Exception("Search bar not found")
        else:
            return search_bars[0]

    def _sleep_till_page_load(self):
        log_info(f"Waiting for page to load...")
        while True:
            if self.driver.execute_script("return document.readyState") == "complete":
                break
        sleep(2)
