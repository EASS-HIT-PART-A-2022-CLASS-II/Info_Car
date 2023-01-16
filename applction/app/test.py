import json
with open('cars.json') as f:
    data = json.loads(f.read())

data_list = list(data.values())

print(data_list[0])
