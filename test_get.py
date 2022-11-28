import requests
import numpy as np
import yaml
from yaml.loader import SafeLoader

api_url = "http://localhost:1880/get_areas?device_id=OCR_0001"
try:
    response = requests.get(api_url)
    areas_data = response.json()

    with open('./areas.yaml', 'w') as file:
        yaml.dump(areas_data, file)
except :
    with open('./areas.yaml') as f:
        areas_data = yaml.load(f, Loader=SafeLoader)

print(np.asarray(areas_data['areas'], dtype=int))