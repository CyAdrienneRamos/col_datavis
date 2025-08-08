import pandas as pd
import json
import os

# Load CSV from data folder
def load_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join('data', filename))

# Load JSON from data folder
def load_json(filename: str) -> dict:
    with open(os.path.join('data', filename), 'r', encoding='utf-8') as f:
        return json.load(f)

# Main data
dfs = {
    'reg': {
        'fam': load_csv('region_fam.csv'),    # Grouped by family
        'idv': load_csv('region_idv.csv'),    # Adjusted for individuals
        'bin': load_csv('region_bin.csv'),    # Pre-binned for histogram
    },
    'prv': {
        'fam': load_csv('province_fam.csv'),
        'idv': load_csv('province_idv.csv'),
        'bin': load_csv('province_bin.csv'),
    }
}

# GeoJSON data
geojson_reg = load_json('RegionsOriginal.json')
geojson_prv = load_json('ProvincesOriginal.json')

region_list = dfs['reg']['idv']['region_name'].tolist()
province_list = dfs['prv']['idv']['province_name'].tolist()