import requests
ip = requests.get("http://myip.azurewebsites.net")
r = requests.get("http://update.dnsexit.com/RemoteUpdate.sv?login=cdesewell&password=HorseKick12&host=pi.chrissewell.co.uk&myip=" + ip.text)
print(r.text)
