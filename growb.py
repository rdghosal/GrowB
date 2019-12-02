import sys
from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException


class GrowB():
    """
    Singleton to initiate and execute backup
    """
    def __init__(self, url, driver, user, pw):
        self.__url = url
        self.__driver = self._init_driver(driver)
        self.__creds = Credentials(user, pw)

    def get_creds(self):
        """Prompt user to input GROWI login credentials"""
        if not self.__creds.user or not self.__creds.pw:
            # TODO: Verify credentials
            user = input("username: ")
            pw = getpass("password: ")
            self.__creds.user = user
            self.__creds.pw = pw

    def _get_driver(self):
        """Gets driver from user input"""
        driver = ""
        valid_drivers = ["firefox", "chrome", "ie", "edge"] # Valid choices

        # Get user selection
        while True:
            print("Select webdriver to use for backup: ")
            for d in valid_drivers:
                print(d)
            print()
            driver = input("Driver: ")
            if driver in valid_drivers:
                break
                
        return driver

    def _init_driver(self, driver=""):
        """Instantiates webdriver instance based on input"""
        if not driver:
            driver = self._get_driver()
        # Switch statement to init driver
        try:
            if driver == "firefox":
                wd = webdriver.Firefox()
            elif driver == "chrome":
                wd = webdriver.Chrome()
            elif driver == "ie":
                wd = webdriver.Ie()
            elif driver == "edge":
                wd = webdriver.Edge()
        except WebDriverException:
            print("ERROR: Driver could not be found. Please check PATH or install selected driver.")
            sys.exit(-1)

        return wd

    def log_in(self):
        """Log on to GROWI using credentials"""
        wd = self.__driver
        wd.get(self.__url[:])

        # Send username
        user_input = wd.find_element_by_xpath("//input[@name='loginForm[username]']")
        user_input.send_keys(self.__creds.user[:])

        # Send password
        pass_input = wd.find_element_by_xpath("//input[@name='loginForm[password]']")
        pass_input.send_keys(self.__creds.pw[:])

        # Search for errors
        try:
            err = wd.find_element_by_xpath("//div[@class='login-form-errors']/div[@class='alert alert-danger']")
            if err:
                print("ERROR: Failed to login with user credentials")
                sys.exit(-1)
        except NoSuchElementException:
            print("Successfully logged on to GROWI")
            



