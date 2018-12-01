import argparse
import sys
import functions
import pprint

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='Find syndication feeds.')
parser.add_argument('url', help='url you want to check for feeds')
args = parser.parse_args()

pprint.pprint(functions.get_rss_feed(args.url))