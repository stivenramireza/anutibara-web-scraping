import sys
sys.path.append('../web-scraping/')
import database
import data_preparation as DataPreparationService
import data_cleaning as DataCleaningService

def main():
    db = database.connect_to_db()
    properties = db.properties
    df = DataPreparationService.convert_collection_to_dataframe(properties)
    DataCleaningService.clean_status(df['status'])
    DataCleaningService.clean_use_status(df['use'])

if __name__ == "__main__":
    main()