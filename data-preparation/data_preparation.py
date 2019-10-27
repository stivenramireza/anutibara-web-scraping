import pandas as pd
from pandas.io.json import json_normalize
import json

def convert_collection_to_dataframe(properties):
    json_documents = list(properties.find({}))
    df_general_info = pd.DataFrame(json_documents, 
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
    df_location = json_normalize(json_documents, 'location')
    df_owner_property = json_normalize(json_documents, 'ownerProperty')
    df_features = json_normalize(json_documents, 'features')
    df_more_features = json_normalize(json_documents, 'moreFeatures')
    df_offers_type = json_normalize(json_documents, 'offersType')
    df = pd.concat([df_general_info, df_location, df_owner_property, 
                    df_features, df_more_features, df_offers_type], axis=1)
    print(df.columns)