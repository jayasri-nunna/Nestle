import requests
import json

base_url = "https://petstore.swagger.io/v2/"
header = {'Content-Type' : 'application/json'}

#reading payload file as f and loading it into payload variable
with open('user_creation_payload.json', 'r') as f:
  payload = json.load(f)

#creating user details
create_user = requests.post(url=base_url+"user", headers=header, json=payload)

#Handling user creation failure
if create_user.status_code == 200:
    print("User created successfully.")
else:
    print(f"User creation failed with status code: {create_user.status_code}")


username = payload.get('username')
#retrieve created user data
get_user= requests.get(url=base_url+"user/"+username, headers=header)

"""print(get_user.text)"""