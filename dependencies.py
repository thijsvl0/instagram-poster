import os
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_env():
    load_dotenv(os.path.join(ROOT_DIR,'.env'))

def main():
    load_env()

if __name__ == 'dependencies':
    main()