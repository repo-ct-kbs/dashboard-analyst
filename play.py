import json

with open('dataset_user.json', 'r') as file:
    datas = json.load(file)

for item in datas:
    print(item['country']['country_code_alpha'])