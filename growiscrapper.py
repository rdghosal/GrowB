import mechanicalsoup
from getpass import getpass

class GrowiScrapper():
    """
    Singleton to initiate and execute backup
    """
    def __init__(self, url, driver, user, pw):
        self.__url = url
        self.__browser = mechanicalsoup.StatefulBrowser()
        self.__creds = Credentials(user, pw)
        self.__logged_in = False

    def get_creds(self):
        """Prompt user to input GROWI login credentials"""
        if not self.__creds.user or not self.__creds.pw:
            # Creds are verified @ log in
            user = input("username: ")
            pw = getpass("password: ")
            self.__creds.user = user
            self.__creds.pw = pw

    def log_in(self):
        """Log on to GROWI using credentials"""
        # Pointer to browser
        # and open URL to GROWI instance
        b = self.__browser
        b.open(self.__url)

        # Grab login form, fill in, and submit
        b.select_form("form[action='/login']")
        b["loginForm[username]"] = self.__creds.user[:]
        b["loginForm[password]"] = self.__creds.pw[:]
        b.submit_selected()

        # Verify login success
        res_page = b.get_current_page()
        err_container = res_page.find(attrs={"class":"login-form-errors"})

        # Check if page has rendered err messages
        if len(err_container.children) > 0:
            print("ERROR: Failed to login with user credentials")
        else: 
            print("Successfully logged on to GROWI")
            self.__logged_in = True
        return self.__logged_in
    
    def check_page(self, target_str):
        """Checks text of page for target str"""
        curr_text = self.__browser.get_current_page().get_text()
        in_curr_page = False
        if curr_text.find(target_str) > -1:
            in_curr_page = True
        return in_curr_page

    def grab_page_links(self):
        """Parses dashboard for links to Wiki pages and returns generator"""
        # Verify whether currently on dashboard
        title = "Welcome to GROWI"
        if not self.__logged_in:
            print("Cannot parse page without logging in")
            raise LoginError
        elif not self.check_page(title):
            print("Could not find dashboard")
            raise WrongPageError

        # Grab contents table to avoid grabbing the same link twice
        table = self.__browser.get_current_page().find("table")
        links = ( a.href for a in table.find_all("a") )

        return links
    
    def scrape_wiki(self, links):
        """Iterates over a links object and scrapes text"""
        # TODO: output as Md by opening MD editor (Typora)
        # TODO: Check libraries for MD conversion

        
class LoginError(Exception):
    pass

class WrongPageError(Exception):
    pass
            

        
        
            
    

