import requests

params = {
    'сheck_url': 'https://www.google.ru/',
    'file_name': 'google',
    'https': 'yes', # Если не указать вернет все прокси
}

response = requests.get('http://31.129.99.16:8080/proxy/generate_and_give', params=params)

print(response)
print(response.json())

#----------------------------------------------------------------

params = {
    'file_name': 'google',
    'https': 'yes', # Если не указать вернет все прокси
}

response = requests.get('http://31.129.99.16:8080/proxy/give_from_file', params=params)

print(response)
print(response.json())


#------------------------------------------------

response = requests.get('http://31.129.99.16:8080/proxy/all_file', params=params)

print(response)
print(response.json())