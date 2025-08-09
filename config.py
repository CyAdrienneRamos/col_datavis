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

VAR_CODING = {
    
}

DEFAULT_CATEGORY = 'col'

DEFAULT_MAPLEVEL = 'reg'