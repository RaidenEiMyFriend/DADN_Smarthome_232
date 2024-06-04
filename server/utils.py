import requests

# Replace these with your Adafruit IO username and key
USERNAME_ = ''
#add your key here
KEY_ = '' 

# List of feed keys for which you want to retrieve data
FEED_KEYS = ['hk232-da-temp', 'hk232-da-light','hk232-da-led','hk232-da-history']

for feed_key in FEED_KEYS:
    url = f'https://io.adafruit.com/api/v2/{USERNAME_}/feeds/{feed_key}/data/last'
    response = requests.get(url, headers={'X-AIO-Key': KEY_})
    data = response.json()

    print(f"Data for Feed {feed_key}:")
    
    if 'value' in data:
        print("  Value:", data['value'])
        print("  Created at:", data['created_at'])
    else:
        print("  No data available or an error occurred.")
    print("-" * 40)


    break

