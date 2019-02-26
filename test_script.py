import json


with open('test.json', 'r') as test_js:
    j_data = test_js.read()

data = json.loads(j_data)

data['Imiona'].append('dupa')
data['nazwiska'].append('cipa')
print(data)

# data2 = json.dumps(data)

with open('test.json', 'w') as test_js:
    test_js.write(data)

test_js.close()
