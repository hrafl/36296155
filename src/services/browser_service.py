from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from pathlib import Path


WAIT_LIMIT = 20 # Time, in seconds, to wait until DOM based commands are considered timed out.

def default_options() -> ChromeOptions:
    options = ChromeOptions()
    # options.add_argument('--headless')
    return options

def create_new_instance(browser_options: ChromeOptions = None) -> Chrome:

    if browser_options is None:
        browser_options = default_options()

    browser = None
    
    try:
        browser = Chrome(chrome_options=browser_options)
    except: 
        try:
            drive_file = f"{Path.cwd()}\\web_drivers\\chromedriver.exe"
            browser = Chrome(executable_path=drive_file, chrome_options=browser_options)
        except: pass
    
    if not browser is None:
        browser.implicitly_wait(WAIT_LIMIT)
    
    return browser

def is_page_loading_complete(browser: WebDriver) -> bool:
    page_state = browser.execute_script('return document.readyState;')
    if page_state == 'complete':
        return True
    else:
        return False

def wait_until_page_is_loaded(browser: WebDriver):
    while True:
        if is_page_loading_complete(browser):
            return