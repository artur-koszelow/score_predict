import json
import pandas as pd

with open('matches.json', 'r') as test_js:
    j_data = test_js.read()

df = pd.read_json(j_data)

hosts = pd.get_dummies(df['host'])
guests = pd.get_dummies(df['guest'])

comps_dummies = hosts.add(guests, fill_value=0).astype('uint8')


with open('comps_dummies.json', 'w') as json_file:
    json_file.write(comps_js)
json_file.close()

# print(df)
# data2 = json.dumps(data)
#
# with open('matches_test.json', 'w') as json_file:
#     json_file.write(data2)
# json_file.close()


# len1 = len(data['day'])
# print(len1)
# for i in data:
#     print(len(data[i]), i)
#     # del data[i][-54:]


#     # print(len(data[i]))
# len2 = len1 - len(data['day'])
# print(len2)


# print(data['day'].count(14))
# print(data['day'])
