import sys
sys.path.append('../web-scraping/')
import database
import data_preparation as DataPreparationService
import data_cleaning as DataCleaningService

def main():
    db = database.connect_to_db()
    properties = db.properties
    dataframe = DataPreparationService.convert_collection_to_dataframe(properties)
    DataCleaningService.clean_data(dataframe)

if __name__ == "__main__":
    main()