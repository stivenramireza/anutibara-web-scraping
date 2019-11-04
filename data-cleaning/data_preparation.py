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

    # Location DataFrame
    df_location = json_normalize(new_properties_json, record_path='location', meta='urlProperty')
    ddf_location = dd.from_pandas(df_location, npartitions=10)

    # Owner Property DataFrame
    df_owner_property = json_normalize(new_properties_json, record_path='ownerProperty', meta='urlProperty')
    ddf_owner_property = dd.from_pandas(df_owner_property, npartitions=10)

    # Features DataFrame
    df_features = json_normalize(new_properties_json, record_path='features', meta='urlProperty')
    ddf_features = dd.from_pandas(df_features, npartitions=10)
    new_columns = ['admon_price', 'antiquity', 'general_bathrooms', 'condition', 'construction_area',
                'floor', 'garages', 'includes_administration', 'interior_floors', 'range_prices', 
                'range_private_area', 'general_rooms', 'square_meters', 'square_meters_price', 'stratum', 
                'weather', 'urlProperty']
    ddf_features = ddf_features.rename(columns=dict(zip(ddf_features.columns, new_columns)))

    # More Features DataFrame
    df_more_features = json_normalize(new_properties_json, record_path='moreFeatures', meta='urlProperty')
    ddf_more_features = dd.from_pandas(df_more_features, npartitions=10)

    # Concat DataFrames into New Properties DataFrame
    ddf_list = [ddf_general_info, ddf_location, ddf_owner_property, ddf_features, ddf_more_features]
    ddf = concat_dataframes(ddf_list, 'urlProperty', True)

    # Remove Repeated Columns
    ddf_new_properties = remove_repeated_columns(ddf)
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
    return ddf_old_properties

def rename_new_properties_column(dataframe):
    new_columns = ['area', 'bathrooms', 'offer_type', 'price', 'private_area',
               'property', 'rooms', 'id_mongoose', 'id_property', 'scraping_date', 
               'scraping_hour', 'modify_hour', 'modify_date', 'code', 'active', 'type',
               'new_property', 'name_project', 'description', 'address', 'city', 'country', 
               'department', 'latitude', 'longitude', 'neighborhood', 'sector', 'contract_type',
               'financing', 'id', 'name', 'schedule', 'admon_price', 'antiquity', 'general_bathrooms',
               'condition', 'construction_area', 'floor', 'garages', 'includes_administration', 
               'interior_floors', 'range_prices', 'range_private_area', 'general_rooms', 'square_meters',
               'square_meters_price', 'stratum', 'weather', 'exterior_features', 'interior_features', 
               'sector_features']
    renamed_dataframe = rename_columns(new_columns, dataframe)
    return renamed_dataframe

def rename_old_properties_column(dataframe):
    new_columns = ['id_mongoose', 'id_property', 'scraping_date', 
               'scraping_hour', 'modify_hour', 'modify_date', 'code', 'active', 'type',
               'new_property', 'name_project', 'description', 'address', 'city', 'country', 
               'department', 'latitude', 'longitude', 'neighborhood', 'sector', 'contract_type',
               'financing', 'id', 'name', 'schedule', 'admon_price', 'antiquity', 'bathrooms',
               'condition', 'construction_area', 'floor', 'garages', 'includes_administration', 
               'interior_floors', 'price', 'private_area', 'rooms', 'square_meters',
               'square_meters_price', 'stratum', 'weather', 'exterior_features', 'interior_features', 
               'sector_features']
    renamed_dataframe = rename_columns(new_columns, dataframe)
    return renamed_dataframe

def remove_repeated_columns(dataframe):
    return dataframe.loc[:,~dataframe.columns.duplicated()]

def concat_dataframes(list_dataframes, index, has_index):
    if(has_index):
        for ddf in list_dataframes:
            ddf.set_index(index)
    ddf = dd.concat(list_dataframes, axis=1)
    ddf.reset_index()
    return ddf

def rename_columns(list_columns, dataframe):
    dataframe = dataframe.rename(columns=dict(zip(dataframe.columns, list_columns)))
    return dataframe

def clean_data(properties):
    df_new_properties = convert_new_properties_to_dataframe(properties)
    df_old_properties = convert_old_properties_to_dataframe(properties)
    df_renamed_new_properties = rename_new_properties_column(df_new_properties)
    df_renamed_old_properties = rename_old_properties_column(df_old_properties)
    df_cleaned_new_properties = DataCleaningService.clean_new_properties_dataframe(df_renamed_new_properties)
    df_cleaned_old_properties = DataCleaningService.clean_old_properties_dataframe(df_renamed_old_properties)