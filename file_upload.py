import requests

url = url = 'http://up.hydrax.net/87d61f1f4fcb4a5397130d26b30a24de'

file_name = 'demo.mp4'
file_type = 'video/mp4'
file_path = './demo.mp4'
files = {'file': (file_name, open(file_path, 'rb'), file_type)}

r = requests.post(url, files=files)
print(r.text)
