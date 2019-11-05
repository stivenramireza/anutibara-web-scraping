import pandas as pd
from pandas.io.json import json_normalize
import data_cleaning as DataCleaningService
import json
import dask.dataframe as dd

def convert_new_properties_to_dataframe(properties):
    new_properties_json = list(properties.find({ 'use': 'Nuevo' }))

    # General Info DataFrame
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
    ddf_general_info = dd.from_pandas(df_general_info, npartitions=10)
    ddf_general_info = ddf_general_info.rename(columns={
        'offerType': 'offer_type'
    })

    # Location DataFrame
    df_location = json_normalize(new_properties_json, record_path='location', meta='urlProperty')
    ddf_location = dd.from_pandas(df_location, npartitions=10)

    # Owner Property DataFrame
    df_owner_property = json_normalize(new_properties_json, record_path='ownerProperty', meta='urlProperty')
    ddf_owner_property = dd.from_pandas(df_owner_property, npartitions=10)

    # Features DataFrame
    df_features = json_normalize(new_properties_json, record_path='features', meta='urlProperty')
    ddf_features = dd.from_pandas(df_features, npartitions=10)
    ddf_features = ddf_features.rename(columns={
        'price':'range_prices',
        'rooms': 'general_rooms',
        'bathrooms': 'general_bathrooms',
        'privateArea': 'range_private_area'
    })

    # More Features DataFrame
    df_more_features = json_normalize(new_properties_json, record_path='moreFeatures', meta='urlProperty')
    ddf_more_features = dd.from_pandas(df_more_features, npartitions=10)

    # Concat DataFrames into New Properties DataFrame
    ddf_list = [ddf_general_info, ddf_location, ddf_owner_property, ddf_features, ddf_more_features]
    ddf = concat_dataframes(ddf_list, 'urlProperty', True)

    # Remove Repeated Columns
    ddf_new_properties = remove_repeated_columns(ddf)

    # Rename Columns
    ddf_new_properties = rename_columns(ddf_new_properties)
    return ddf_new_properties

def convert_old_properties_to_dataframe(properties):
    old_properties_json = list(properties.find({ 'use': 'Usado' }))

    # General Info DataFrame
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
                                    'description'])
    ddf_general_info = dd.from_pandas(df_general_info, npartitions=10)

    # Location DataFrame
    df_location = json_normalize(old_properties_json, 'location')
    ddf_location = dd.from_pandas(df_location, npartitions=10)

    # Owner Property DataFrame
    df_owner_property = json_normalize(old_properties_json, 'ownerProperty')
    ddf_owner_property = dd.from_pandas(df_owner_property, npartitions=10)

    # Features DataFrame
    df_features = json_normalize(old_properties_json, 'features')
    ddf_features = dd.from_pandas(df_features, npartitions=10)

    # More Features DataFrame
    df_more_features = json_normalize(old_properties_json, 'moreFeatures')
    ddf_more_features = dd.from_pandas(df_more_features, npartitions=10)

    # Concat DataFrames into Old Properties DataFrame
    ddf_list = [ddf_general_info, ddf_location, ddf_owner_property, ddf_features, ddf_more_features]
    ddf = concat_dataframes(ddf_list, '', False)

    # Remove Repeated Columns
    ddf_old_properties = remove_repeated_columns(ddf)

    # Rename Columns
    ddf_old_properties = rename_columns(ddf_old_properties)
    return ddf_old_properties

def remove_repeated_columns(dataframe):
    return dataframe.loc[:,~dataframe.columns.duplicated()]

def concat_dataframes(list_dataframes, index, has_index):
    if(has_index):
        for ddf in list_dataframes:
            ddf.set_index(index)
    ddf = dd.concat(list_dataframes, axis=1)
    ddf.reset_index()
    return ddf

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
    })
    return dataframe

def clean_data(properties):
    df_new_properties = convert_new_properties_to_dataframe(properties)
    df_old_properties = convert_old_properties_to_dataframe(properties)
    df_cleaned_new_properties = DataCleaningService.clean_new_properties_dataframe(df_new_properties)
    print(df_cleaned_new_properties.columns)
    df_cleaned_old_properties = DataCleaningService.clean_old_properties_dataframe(df_old_properties)
    print(df_cleaned_old_properties.columns)