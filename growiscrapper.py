import mechanicalsoup, os
from getpass import getpass
from datetime import date

class GrowiScrapper():
    """
    Singleton to initiate and execute backup
    """
    def __init__(self, url, driver, user, pw):
        self.__root = url
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
        b.open(self.__root)

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
        try:
            title = "Welcome to GROWI"
            if not self.__logged_in:
                raise LoginError
            elif not self.check_page(title):
                raise WrongPageError

            # Grab contents table to avoid grabbing the same link twice
            table = self.__browser.get_current_page().find("table")
            links = ( a.href for a in table.find_all("a") )
            return links

        except LoginError:
            print("Cannot parse page without logging in")
        except WrongPageError:
            print("Could not find dashboard")
    
    def _get_filename(self, link):
        """Parse link to make filename for output file"""
        
    
    def scrape_wikis(self, links, to_md=False, dest_path=""):
        """Iterates over a links object and scrapes text"""
        # TODO: output as Md by opening MD editor (Typora)
        # TODO: Check libraries for MD conversion

        b = self.__browser
        # dashboard_url = b.get_url()

        # Use default path if not provided
        if not dest_path:
            growb_path = os.path.join(os.getenv("HOME"), "GrowB")
            os.mkdir(growb_path)
            dest_path = growb_path

            # TODO: Make as alt feature? 
            # Make folder for date of execution,
            # folder name being "MMddyy"
            # today = date.strftime(date.today(), "%m%d%y")            
            # dest_path = os.path.join(growb_path, today)
            # os.mkdir(dest_path)

        print(f"Writing the following files in {dest_path}")

        file_cnt = 1
        for link in links:
            # Navigate from dashboard to wiki
            abs_url = os.path.join(self.__root[:], link[:])
            b.open(abs_url)

            # Because <a> hrefs are illegible,
            # using curr url instead to assign file/folder names 
            curr_url = str(self.__browser.get_url())

            # Calculate end index of root url
            # and grab everything but root
            root_end = curr_url.index(self.__root) + len(self.__root)
            filename = curr_url[root_end:]

            # To store subdir folder names
            subdirs = []

            # Set dest folder by parsing link
            # and path names if within a dir
            if filename.find("/") > -1:
                frags = filename.split("/")
                filename = frags[-1]
                subdirs = frags[1:-1] # Starts from index 1 to avoid empty str

            # Parse soup for the wiki <div> container
            soup = self.__browser.get_current_page()
            wiki_container = soup.find("div", {"class": "wiki"})

            # To hold soup contents as string
            wiki_contents = ""
            if to_md:
                contents = wiki_container.contents
                wiki_contents = "".join(contents)
            else:
                wiki_contents = wiki_container.get_text() 

            ext = ".md" if to_md else ".txt"
            filename += ext

            # Concatenate file path in order of parsed dir names
            dir_str = ""
            for dir_ in subdirs:
                dir_str += dir_
                os.mkdir(os.path.join(dest_path, dir_str))
                # TODO: use os.path.exists

            # Save contents
            path = os.path.join(dest_path, dir_str, filename)
            with open(path, "w") as f:
                f.write(wiki_contents)
            print(f"  Wrote {filename} in {dest_path}")
            file_cnt += 1

        print()
        print(f"Wrote {file_cnt} wikis in {dest_path}")
        
        
class LoginError(Exception):
    pass


class WrongPageError(Exception):
    pass
            

        
        
            
    

