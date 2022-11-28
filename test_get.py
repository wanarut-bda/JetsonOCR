import requests
import numpy as np
api_url = "http://localhost:1880/get_areas?device_id=OCR_0001"
response = requests.get(api_url)
print(np.asarray(response.json()['areas'], dtype=int))