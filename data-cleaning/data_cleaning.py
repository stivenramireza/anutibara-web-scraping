import re
from re import sub
from decimal import Decimal

def clean_active(column):
    return column.apply(lambda status: True if (status == 'Active') else False)

def clean_new_property(column):
    return column.apply(lambda status: True if (status == 'Nuevo') else False)

def clean_includes_administration(column):
    return column.apply(lambda status: True if (status == 'Nuevo') else False)

def clean_garages(column):
    column = column.replace('', value = 0, regex = True)
    column = column.replace('Más de 10', value = 0, regex = True)
    return column.astype(int)

def clean_stratum(column):
    column = column.replace('', value = 0, regex = True)
    column = column.replace('Campestre', value = 0, regex = True)
    return column.astype(int)

def clean_floor(column):
    return column.astype(int)

def clean_area(column):
    return column.astype(float)

def clean_price(column):
    return column.apply(lambda price: Decimal(sub(r'[^\d,]', '', price))).astype(int)

def clean_square_meters(column):
    column = column.str[0:-3]
    column = column.apply(lambda meters: Decimal(sub(r'[^\d,]', '', meters)))
    return column.astype(float)

def clean_rooms(column):
    return column.astype(int)

def clean_bathrooms(column):
    return column.astype(int)

def clean_new_private_area(column):
    column = column.replace('', value = 0, regex = True)
    return column.astype(float)

def clean_old_private_area(column):
    column = column.str[0:-2]
    column = column.replace('', value = '0', regex = True)
    column = column.apply(lambda area: Decimal(sub(r'[^\d.]', '', area)))
    return column.astype(float)

def clean_construction_area(column):
    column = column.str[0:-3]
    column = column.apply(lambda area: Decimal(sub(r'[^\d,]', '', area)))
    return column.astype(float)

def clean_general_columns(dataframe):
    cleaned_dataframe = dataframe
    clean_active(cleaned_dataframe['active'])
    clean_new_property(cleaned_dataframe['new_property'])
    clean_includes_administration(cleaned_dataframe['includes_administration'])
    clean_garages(cleaned_dataframe['garages'])
    clean_stratum(cleaned_dataframe['stratum'])
    clean_floor(cleaned_dataframe['floor'])
    clean_price(cleaned_dataframe['price'])


def clean_new_properties_dataframe(dataframe):
    cleaned_dataframe = dataframe
    clean_area(cleaned_dataframe['area'])
    clean_rooms(cleaned_dataframe['rooms'])
    clean_bathrooms(cleaned_dataframe['bathrooms'])
    clean_new_private_area(cleaned_dataframe['private_area'])
    clean_general_columns(cleaned_dataframe)
    return cleaned_dataframe

def clean_old_properties_dataframe(dataframe):
    cleaned_dataframe = dataframe
    clean_square_meters(cleaned_dataframe['square_meters'])
    clean_old_private_area(cleaned_dataframe['private_area'])
    clean_construction_area(cleaned_dataframe['construction_area'])
    clean_general_columns(cleaned_dataframe)
    return cleaned_dataframe