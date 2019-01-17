import requests

url = "http://localhost"

# To get list of all entries, GET

rel = requests.get(url)
print(rel.text)

# To get list of one specific entry, given the ID, GET

id = '1'.encode()
rev = requests.get(url, data = id)
print(rev.text)

# To add a string to the file, POST

dc = b'hello world. I am created'
rec = requests.post(url, data = dc)
print(rec.text)

# To uppdate a record, given its id and the data to be updated, PUT

du = b'Hello world. I am updated.'
reu = requests.put(url, data = {'id':1, 'data':du })
print(reu.text)

# To delete a record given its data.

dd = b'Hello world. I am updated.'
red = requests.delete(url, data = dd)
print(red.text)