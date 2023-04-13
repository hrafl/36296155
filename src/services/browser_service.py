from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Edge, EdgeOptions, Safari
from selenium.webdriver.remote.webdriver import WebDriver

WAIT_LIMIT = 20 # Time, in seconds, to wait until DOM based commands are considered timed out.

def create_new_instance() -> WebDriver:

    browser = None
    
    try:
        browser = __create_new_chrome_instance__()
    except:
        try:
            browser = __create_new_firefox_instance__()
        except:
            try:
                browser = __create_edge_instance__()
            except:
                try:
                    browser = __create_safari_instance__()
                except:
                    raise Exception("Could not create browser object in browser_service.py")
    
    if not browser is None:
        browser.maximize_window()
        browser.implicitly_wait(WAIT_LIMIT)
    
    return browser
    

def __create_new_chrome_instance__() -> Chrome:
    options = ChromeOptions()
    # options.add_argument('--headless')
    browser = Chrome(chrome_options=options)
    return browser

def __create_new_firefox_instance__() -> Firefox:
    options = FirefoxOptions()
    # options.add_argument('--headless')
    browser = Firefox(options=options)
    return browser

def __create_edge_instance__() -> Edge:
    options = EdgeOptions()
    options.add_argument('--headless')
    browser = Edge(options=options)
    return browser

def __create_safari_instance__() -> Safari:
    browser = Safari()
    return browser

# ----------------------------------------------

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