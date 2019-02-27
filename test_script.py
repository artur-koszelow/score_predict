import json
from pandas import DataFrame

with open('matches.json', 'r') as test_js:
    j_data = test_js.read()

data = json.loads(j_data)
df = DataFrame(data)

print(df)