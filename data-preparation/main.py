import sys
sys.path.append('../web-scraping/')
import database as database

def main():
    db = database.connect_to_db()

if __name__ == "__main__":
    main()