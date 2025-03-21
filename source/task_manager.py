# main.py

import argparse
from textes import WELCOME_MESSAGE, HELP_TEXT, ERROR_MESSAGE

def main():
    print(WELCOME_MESSAGE)
    
    parser = argparse.ArgumentParser(description="Une application CLI simple.")
    parser.usage = HELP_TEXT
    parser.add_argument("-h", "--help", action="store_true", help="Affiche l'aide.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles.")

    args = parser.parse_args()

    if args.help:
        print(HELP_TEXT)
    elif args.version:
        print(VERSION_TEXT)
    else:
        print(ERROR_MESSAGE)

if __name__ == "__main__":
    main()
