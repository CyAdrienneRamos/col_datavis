import pandas as pd
import json
import os

PRV_TO_REG = {
    'Abra': 'Cordillera Administrative Region',
    'Agusan del Norte': 'Region XIII - Caraga',
    'Agusan del Sur': 'Region XIII - Caraga',
    'Aklan': 'Region VI - Western Visayas',
    'Albay': 'Region V- Bicol',
    'Antique': 'Region VI - Western Visayas',
    'Apayao': 'Cordillera Administrative Region',
    'Aurora': 'Region III - Central Luzon',
    'Basilan': 'Region IX - Zamboanga Peninsula',
    'Bataan': 'Region III - Central Luzon',
    'Batanes': 'Region II - Cagayan Valley',
    'Batangas': 'Region IVA - CALABARZON',
    'Benguet': 'Cordillera Administrative Region',
    'Biliran': 'Region VIII - Eastern Visayas',
    'Bohol': 'Region VII - Central Visayas',
    'Bukidnon': 'Region X - Northern Mindanao',
    'Bulacan': 'Region III - Central Luzon',
    'Cagayan': 'Region II - Cagayan Valley',
    'Camarines Norte': 'Region V- Bicol',
    'Camarines Sur': 'Region V- Bicol',
    'Camiguin': 'Region X - Northern Mindanao',
    'Capiz': 'Region VI - Western Visayas',
    'Catanduanes': 'Region V- Bicol',
    'Cavite': 'Region IVA - CALABARZON',
    'Cebu': 'Region VII - Central Visayas',
    'Compostela Valley': 'Region XI - Davao',
    'Davao Oriental': 'Region XI - Davao',
    'Davao del Norte': 'Region XI - Davao',
    'Davao del Sur': 'Region XI - Davao',
    'Dinagat Islands': 'Region XIII - Caraga',
    'Eastern Samar': 'Region VIII - Eastern Visayas',
    'Guimaras': 'Region VI - Western Visayas',
    'Ifugao': 'Cordillera Administrative Region',
    'Ilocos Norte': 'Region I - Ilocos Region',
    'Ilocos Sur': 'Region I - Ilocos Region',
    'Iloilo': 'Region VI - Western Visayas',
    'Isabela': 'Region II - Cagayan Valley',
    'Kalinga': 'Cordillera Administrative Region',
    'La Union': 'Region I - Ilocos Region',
    'Laguna': 'Region IVA - CALABARZON',
    'Lanao del Norte': 'Region X - Northern Mindanao',
    'Lanao del Sur': 'Bangsamoro Autonomous Region in Muslim Mindanao',
    'Leyte': 'Region VIII - Eastern Visayas',
    'Maguindanao': 'Bangsamoro Autonomous Region in Muslim Mindanao',
    'Marinduque': 'Region IVB - MIMAROPA',
    'Masbate': 'Region V- Bicol',
    'Metropolitan Manila': 'National Capital Region',
    'Misamis Occidental': 'Region X - Northern Mindanao',
    'Misamis Oriental': 'Region X - Northern Mindanao',
    'Mountain Province': 'Cordillera Administrative Region',
    'Negros Occidental': 'Region VI - Western Visayas',
    'Negros Oriental': 'Region VII - Central Visayas',
    'North Cotabato': 'Region XII - SOCCSKSARGEN',
    'Northern Samar': 'Region VIII - Eastern Visayas',
    'Nueva Ecija': 'Region III - Central Luzon',
    'Nueva Vizcaya': 'Region II - Cagayan Valley',
    'Occidental Mindoro': 'Region IVB - MIMAROPA',
    'Oriental Mindoro': 'Region IVB - MIMAROPA',
    'Palawan': 'Region IVB - MIMAROPA',
    'Pampanga': 'Region III - Central Luzon',
    'Pangasinan': 'Region I - Ilocos Region',
    'Quezon': 'Region IVA - CALABARZON',
    'Quirino': 'Region II - Cagayan Valley',
    'Rizal': 'Region IVA - CALABARZON',
    'Romblon': 'Region IVB - MIMAROPA',
    'Samar': 'Region VIII - Eastern Visayas',
    'Sarangani': 'Region XII - SOCCSKSARGEN',
    'Siquijor': 'Region VII - Central Visayas',
    'Sorsogon': 'Region V- Bicol',
    'South Cotabato': 'Region XII - SOCCSKSARGEN',
    'Southern Leyte': 'Region VIII - Eastern Visayas',
    'Sultan Kudarat': 'Region XII - SOCCSKSARGEN',
    'Sulu': 'Bangsamoro Autonomous Region in Muslim Mindanao',
    'Surigao del Norte': 'Region XIII - Caraga',
    'Surigao del Sur': 'Region XIII - Caraga',
    'Tarlac': 'Region III - Central Luzon',
    'Tawi-Tawi': 'Bangsamoro Autonomous Region in Muslim Mindanao',
    'Zambales': 'Region III - Central Luzon',
    'Zamboanga Sibugay': 'Region IX - Zamboanga Peninsula',
    'Zamboanga del Norte': 'Region IX - Zamboanga Peninsula',
    'Zamboanga del Sur': 'Region IX - Zamboanga Peninsula',
}

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
    },
    'pri' : load_csv('price_filtered.csv')       # Food prices
}
dfs['pri'] = dfs['pri'].map(lambda x: 'N/A' if x == 0 else x)

# GeoJSON data
geojson_reg = load_json('RegionsOriginal.json')
geojson_prv = load_json('ProvincesOriginal.json')

region_list = dfs['reg']['idv']['region_name'].tolist()
province_list = dfs['prv']['idv']['province_name'].tolist()