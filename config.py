from data_loader import geojson_prv, geojson_reg

# Mapping level selector details
MAP_LEVEL_SETTINGS = {
    'reg': {
        'feature': 'properties.REGION',
        'geojson': geojson_reg,
        'grouper': 'region_name',
    },
    'prv': {
        'feature': 'properties.NAME_1',
        'geojson': geojson_prv,
        'grouper': 'province_name',
    }
}

# Default selection for maps
DEFAULT_MAP_SELECTION = {
    'reg': "National Capital Region",
    'prv': "Metropolitan Manila"
}


DEFAULT_CATEGORY = 'col'

DEFAULT_MAPLEVEL = 'reg'

VARIABLE_EXPANSION = {
    'col': 'Cost of Living',
    'food': 'Food Expense',
    'housing': 'Housing and Utilities Expense',
    'transport': 'Transportation Expense',
}

def get_figline_title(category):
    return f'Median {VARIABLE_EXPANSION[category]} by Family Size'

def get_fighist_title(category):
    return f'{VARIABLE_EXPANSION[category]} Distribution'