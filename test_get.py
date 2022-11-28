import requests
api_url = "http://localhost:1880/get_areas?device_id=OCR_0001"
response = requests.get(api_url)
print(response.json()['areas'])