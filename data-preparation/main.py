import sys
sys.path.insert(0, "../web-scraping/database")
import database as database

def main():
    db = database.connect_to_db()

if __name__ == "__main__":
    main()