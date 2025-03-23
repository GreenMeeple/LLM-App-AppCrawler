
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Run app store crawlers")
    parser.add_argument('--store', choices=['appstore', 'playstore'], required=True, help="Choose which store to crawl")

    args = parser.parse_args()
    root_dir = os.path.dirname(os.path.abspath(__file__))

    if args.store == 'appstore':
        sys.path.insert(0, os.path.join(root_dir, 'AppStore'))
        from util.appStore_crawl import run_as
        run_as()

    elif args.store == 'playstore':
        sys.path.insert(0, os.path.join(root_dir, 'PlayStore'))
        from util.playStore_crawl import run_ps
        run_ps()

if __name__ == "__main__":
    main()
