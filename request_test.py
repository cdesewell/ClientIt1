import requests
r = requests.get("http://runtimeit1.azurewebsites.net/api/runtime")
print(r.text)
