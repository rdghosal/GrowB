#!usr/env/bin python3
import sys, os, argparse
from growiscraper import GrowiScraper 


def main(args):
    """Uses GrowiScrapper singleton to scrape designated url
    and output either text or Markdown files"""
    scraper = GrowiScraper(args.url)
    scraper.get_creds()
    if scraper.log_in():
        links = scraper.grab_page_links()
        dest_path = args.path

        # Default behavior if no path specified
        if not dest_path:
            growb_path = os.path.join(os.getenv("HOME"), "GrowB")
            if not os.path.exists(growb_path):
                os.mkdir(growb_path)
            dest_path = growb_path

            # TODO: Make as alt feature? 
            # Make folder for date of execution,
            # folder name being "MMddyy"
            # today = date.strftime(date.today(), "%m%d%y")            
            # dest_path = os.path.join(growb_path, today)
            # os.mkdir(dest_path)

        scraper.scrape_wikis(links=links, to_md=args.to_md, dest_path=dest_path)
        return 0
    else:
        # Error: Login failed
        return -1


if __name__ == "__main__":
    desc = """GrowiB backs up wiki files in a GROWI instance
            into the local file directory.
            Format defaults to textfile unless indicated"""

    # Help msg
    parser = argparse.ArgumentParser(description=desc)

    # Positional args 
    parser.add_argument("url", nargs=1, help="URL to GROWI instance")
    
    # Optional args
    parser.add_argument("-p", "--path", nargs=1, help="Path for destination files")
    parser.add_argument("--to_md", action="store_true", help="Use for .md file output")

    args = parser.parse_args()
    code = main(args)

    if code == -1:
        # Failure
        print("An error occurred. Check login credentials or GROWI instance and try again")
    else:
        # Success
        _ = input("Press any key to close the program")

    sys.exit(code)