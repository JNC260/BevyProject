import modules
import sys

def analyze_feed(url):
    modules.get_rss_feed(url)



analyze_feed("https://www.google.com/")

# if __name__ == '__main__':
#     # Map command line arguments to function arguments.
#     analyze_feed(*sys.argv[1:])