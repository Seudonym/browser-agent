import marimo

__generated_with = "0.12.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    return By, mo, webdriver


@app.cell
def _(webdriver):
    driver = webdriver.Chrome()
    return (driver,)


@app.cell
def _(By, driver):
    driver.get("https://github.com")
    from time import sleep
    sleep(2)
    def _find_button_by_text(text: str, fuzzy: bool = True):

        def filter_func(x):
            extracted_text = x.text
            # print(extracted_text)
            if extracted_text.strip() == "":
                extracted_text = x.get_attribute("value")
            if not extracted_text: return False
            if fuzzy:
                return text.lower() in extracted_text.lower()
            else:
                return text == extracted_text

        anchors = driver.find_elements(By.TAG_NAME, "a")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        buttons = driver.find_elements(By.TAG_NAME, "button")

        candidates = anchors + inputs + buttons
        # print(candidates)
        candidates = filter(filter_func, candidates)
        candidates = list(candidates)
        if len(candidates) == 0:
            raise Exception("Element not found")
        else:
            return candidates[0]
    _find_button_by_text("Sign In")
    return (sleep,)


@app.cell
def _(By, driver):
    text = "Sign in"
    def filter_func(x):
        extracted_text = x.text
        print(f"Extracted text: {extracted_text}")
        if extracted_text.strip() == "":
            extracted_text = x.get_attribute("value")
        if False:
            return text.lower() in extracted_text.lower()
        else:
            return text == extracted_text

    anchors = driver.find_elements(By.TAG_NAME, "a")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    candidates = list(filter(filter_func, anchors + inputs + buttons))

    return anchors, buttons, candidates, filter_func, inputs, text


@app.cell
def _(inputs):
    inputs[0].get_attribute('value')
    return


@app.cell
def _(anchors):
    dir(anchors[0])
    return


@app.cell
def _(anchors):
    filtered = list(filter(lambda x: x.text.lower() == "sign in", anchors))
    [x.text for x in filtered]
    return (filtered,)


@app.cell
def _(By, driver):
    [x.accessible_name for x in driver.find_elements(By.TAG_NAME, 'input')]
    return


@app.cell
def _(By, driver):
    search_bars =  list(filter(lambda x: x.get_attribute(
                "type") == "text", driver.find_elements(By.TAG_NAME, "input")))
    return (search_bars,)


if __name__ == "__main__":
    app.run()
