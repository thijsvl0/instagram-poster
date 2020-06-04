from dotenv import load_dotenv
import reddit

def main():
    load_dotenv('./.env')

if __name__ == "main":
    main()

if __name__ == "__main__":
    main()
    reddit.main()