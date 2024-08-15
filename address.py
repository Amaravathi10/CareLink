import requests

response = requests.get("https://ipinfo.io/json?token=6d65963c15a531")
data = response.json()
print(data)
