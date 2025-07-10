import requests
import json

base_url = "https://petstore.swagger.io/v2/"
header = {'Content-Type' : 'application/json'}

with open('user_creation_payload.json', 'r') as f:
  payload = json.load(f)

#creating user details
create_user = requests.post(url=base_url+"user", headers=header, json=payload)

#Everytime the create user request results in 200 status code. In real scenario, would handle different status codes

#retrieve created user data
get_user= requests.get(url=base_url+"user/jayasrind")

"""print(get_user.text)"""