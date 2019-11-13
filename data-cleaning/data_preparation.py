import pandas as pd
from pandas.io.json import json_normalize
import data_cleaning as DataCleaningService
import json
import dask.dataframe as dd

list_columns = ['_id', 'urlProperty', 'scrapingDate', 'scrapingHour', 'modifyDate', 'modifyHour', 'code', 'status',  'type',  'use', 
                'nameProject', 'description', 'country', 'department', 'city', 'sector', 'neighborhood', 'address', 'latitude', 'longitude',
                'idOwnerProperty', 'nameOwnerProperty', 'contractType', 'financing', 'schedule', 'price', 'squareMeters', 'rooms', 'bathrooms',
                'garages', 'privateArea', 'constructionArea', 'squareMetersPrice', 'stratum', 'condition', 'antiquity', 'floor', 'interiorFloors',
                'weather', 'includesAdministration', 'admonPrice', 'interiorFeatures', 'exteriorFeatures', 'sectorFeatures']

def convert_new_properties_to_dataframe(list_properties):
    df_new_properties = json_normalize(list_properties, record_path='offersType', 
                                meta=list_columns)
    ddf_new_properties = dd.from_pandas(df_new_properties, npartitions=10)
    ddf_new_properties = remove_repeated_columns(ddf_new_properties)
    ddf_new_properties = remove_nan_rows(ddf_new_properties)
    ddf_new_properties = ddf_new_properties.rename(columns={
        "bathrooms": "general_bathrooms",
        "rooms": "general_rooms",
        "price": "range_prices",
        "squareMeters": "range_square_meters",
        "constructionArea": "range_construction_area",
        "offerType": "offer_type",
        "privateArea": "range_private_area",
        "areaOfferType": "area",
        "bathroomsOfferType": "bathrooms",
        "priceOfferType": "price",
        "privateAreaOfferType": "private_area",
        "roomsOfferType": "rooms"
    })
    # Rename DataFrame
    ddf_new_properties = rename_columns(ddf_new_properties)
    return ddf_new_properties

def convert_old_properties_to_dataframe(list_properties):
    df_old_properties = pd.DataFrame(list_properties, 
                                    columns=list_columns)
    ddf_old_properties = dd.from_pandas(df_old_properties, npartitions=10)
    ddf_old_properties = remove_repeated_columns(ddf_old_properties)
    ddf_old_properties = remove_nan_rows(ddf_old_properties)
    # Rename DataFrame
    ddf_old_properties = rename_columns(ddf_old_properties)
    return ddf_old_properties

def get_properties(properties, type_property):
    return list(properties.find({ 'use': type_property }))

def remove_repeated_columns(dataframe):
    return dataframe.loc[:,~dataframe.columns.duplicated(keep='first')]

def remove_nan_rows(dataframe):
    return dataframe.dropna()

def rename_columns(dataframe):
    dataframe = dataframe.rename(columns={
        "_id": "id_mongoose", 
        "urlProperty":"id_property",
        "scrapingDate": "scraping_date",
        "scrapingHour": "scraping_hour",
        "modifyDate": "modify_date",
        "modifyHour": "modify_hour",
        "status": "active",
        "use": "new_property",
        "nameProject": "name_project",
        "offersType": "offers_type",
        "idOwnerProperty": "id_owner_property",
        "nameOwnerProperty": "name_owner_property",
        "contractType": "contract_type_owner_property",
        "financing": "financing_owner_property",
        "schedule": "schedule_owner_property",
        "squareMetersPrice": "square_meters_price",
        "interiorFloors": "interior_floors",
        "includesAdministration": "includes_administration",
        "admonPrice": "admon_price",
        "interiorFeatures": "interior_features",
        "exteriorFeatures": "exterior_features",
        "sectorFeatures": "sector_features"
    })
    return dataframe

def clean_data(properties):
    list_new_properties = get_properties(properties, 'Nuevo')
    list_old_properties = get_properties(properties, 'Usado')
    df_new_properties = convert_new_properties_to_dataframe(list_new_properties)
    df_old_properties = convert_old_properties_to_dataframe(list_old_properties)
    df_cleaned_new_properties = DataCleaningService.clean_new_properties_dataframe(df_new_properties)
    df_cleaned_old_properties = DataCleaningService.clean_old_properties_dataframe(df_old_properties)