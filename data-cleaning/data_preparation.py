import pandas as pd
from pandas.io.json import json_normalize
import data_cleaning as DataCleaningService
import json

def convert_new_properties_to_dataframe(properties):
    new_properties_json = list(properties.find({ 'use': 'Nuevo' }))
    df_general_info = json_normalize(new_properties_json, record_path='offersType', 
                            meta=['_id', 
                                    'urlProperty', 
                                    'scrapingDate', 
                                    'scrapingHour', 
                                    'modifyDate',
                                    'modifyHour', 
                                    'code', 
                                    'status', 
                                    'type', 
                                    'use', 
                                    'nameProject', 
                                    'description'])
    df_location = json_normalize(new_properties_json, record_path='location', meta='urlProperty')
    df_owner_property = json_normalize(new_properties_json, record_path='ownerProperty', meta='urlProperty')
    df_features = json_normalize(new_properties_json, record_path='features', meta='urlProperty')
    df_features.rename(columns= {
                            "price": "range_prices", 
                            "rooms":"general_rooms",
                            "bathrooms": "general_bathrooms",
                            "privateArea": "range_private_area"
                        }, 
            inplace = True)
    df_more_features = json_normalize(new_properties_json, record_path='moreFeatures', meta='urlProperty')
    df_new_properties = df_general_info.set_index('urlProperty').join(df_location.set_index('urlProperty')).join(df_owner_property.set_index('urlProperty')).join(df_features.set_index('urlProperty')).join(df_more_features.set_index('urlProperty'))
    return df_new_properties

def convert_old_properties_to_dataframe(properties):
    old_properties_json = list(properties.find({ 'use': 'Usado' }))
    df_general_info = pd.DataFrame(old_properties_json, 
                                    columns=['_id', 
                                    'urlProperty', 
                                    'scrapingDate', 
                                    'scrapingHour', 
                                    'modifyDate',
                                    'modifyHour', 
                                    'code', 
                                    'status', 
                                    'type', 
                                    'use', 
                                    'nameProject', 
                                    'description',
                                    'offersType'])
    df_location = json_normalize(old_properties_json, 'location')
    df_owner_property = json_normalize(old_properties_json, 'ownerProperty')
    df_features = json_normalize(old_properties_json, 'features')
    df_more_features = json_normalize(old_properties_json, 'moreFeatures')
    df_old_properties = pd.concat([df_general_info, df_location, df_owner_property, 
                    df_features, df_more_features], axis=1)
    return df_old_properties

def rename_new_properties_column(dataframe):
    dataframe.rename(columns= {
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
                        "id": "id_owner_property",
                        "name": "name_owner_property",
                        "contractType": "contract_type_owner_property",
                        "financing": "financing_owner_property",
                        "schedule": "schedule_owner_property",
                        "squareMeters": "range_square_meters",
                        "constructionArea": "range_construction_area",
                        "squareMetersPrice": "square_meters_price",
                        "interiorFloors": "interior_floors",
                        "includesAdministration": "includes_administration",
                        "admonPrice": "admon_price",
                        "interiorFeatures": "interior_features",
                        "exteriorFeatures": "exterior_features",
                        "sectorFeatures": "sector_features",
                        "offerType": "offer_type",
                        "privateArea": "private_area"
                    }, 
          inplace = True)
    return dataframe

def rename_old_properties_column(dataframe):
    dataframe.rename(columns= {
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
                        "id": "id_owner_property",
                        "name": "name_owner_property",
                        "contractType": "contract_type_owner_property",
                        "financing": "financing_owner_property",
                        "schedule": "schedule_owner_property",
                        "squareMeters": "square_meters",
                        "privateArea": "private_area",
                        "constructionArea": "construction_area",
                        "squareMetersPrice": "square_meters_price",
                        "interiorFloors": "interior_floors",
                        "includesAdministration": "includes_administration",
                        "admonPrice": "admon_price",
                        "interiorFeatures": "interior_features",
                        "exteriorFeatures": "exterior_features",
                        "sectorFeatures": "sector_features"
                    }, 
          inplace = True)
    return dataframe

def clean_data(properties):
    df_new_properties = convert_new_properties_to_dataframe(properties)
    df_old_properties = convert_old_properties_to_dataframe(properties)
    df_renamed_new_properties = rename_new_properties_column(df_new_properties)
    df_renamed_old_properties = rename_old_properties_column(df_old_properties)
    df_cleaned_new_properties = DataCleaningService.clean_new_properties_dataframe(df_renamed_new_properties)
    print(df_cleaned_new_properties.head(10))
    df_cleaned_old_properties = DataCleaningService.clean_old_properties_dataframe(df_renamed_old_properties)
    print(df_cleaned_old_properties.head(10))