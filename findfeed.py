import argparse
import sys
import modules

reload(sys)
sys.setdefaultencoding('utf8')

def analyze_feed(url):
    modules.get_rss_feed(url)

parser = argparse.ArgumentParser(description='Find syndication feeds.')
parser.add_argument('url', help='url you want to check for feeds')
parser.add_argument('--check', const=analyze_feed, action='store_const', help='check for syndication feeds')
args = parser.parse_args()

print(args.check(args.url))