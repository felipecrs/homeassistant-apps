from botasaurus.browser import browser, Driver


@browser(headless=True)
def warm(driver: Driver, data):
    pass


warm()
