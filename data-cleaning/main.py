from multiprocessing import Pool
import sys
sys.path.append('../web-scraping/')
import database
import data_preparation as DataPreparationService

def main():
    db = database.connect_to_db()
    properties = db.properties
    try:
        p = Pool(40)
        p.map(DataPreparationService.clean_data, properties)
        p.terminate()
        p.join()
        print('Data has been cleaned successfully')
    except Exception as e:
        print('Error to prepare and clean data: ', e)

if __name__ == "__main__":
    main()