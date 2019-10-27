import sys
sys.path.append('../web-scraping/')
import database
import data_preparation as DataPreparationService

def main():
    db = database.connect_to_db()
    properties = db.properties
    DataPreparationService.convert_collection_to_dataframe(properties)

if __name__ == "__main__":
    main()