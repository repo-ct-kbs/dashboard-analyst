import requests
import json
import time

api_key = '8c1c4c66fb2c2f955500bb0b7f4e60fc'
max_per_req = 2
url = f'https://api.parser.name/?api_key={api_key}&endpoint=generate&results={max_per_req}'

output_file = 'data_user.json'

def fetch_data():
    all_data = []

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                if data.get('error'):
                    print(f"Error in API response: {data['error']}")
                    break

                all_data.extend(data.get('data', []))

                print("Data fetched successfully.")

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({"results": all_data}, f, ensure_ascii=False, indent=4)

            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

        except requests.RequestException as e:
            print(f"Request failed: {e}")
        
        print("Waiting for 3 seconds before the next attempt...")
        time.sleep(3)
    
fetch_data()
