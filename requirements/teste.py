import requests
headers = {'Ocp-Apim-Subscription-Key' : 'ac533345bca44ec6a811cf5c1721850f'}
url="https://cmlapidev.azure-api.net/coi/mr/qua.1.5.0/coi/entidadesCML/01-01-2020/31-12-2020"       
response_API = requests.get(url,headers=headers)

print(response_API)
