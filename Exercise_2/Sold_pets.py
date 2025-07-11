import requests

from Nestle.Exercise_2.Create_user import base_url, header

#Function to retrieve sold pets
def sold_pets_func():
    sold_pets_list = []
    sold_pets_response = requests.get(url=base_url+"pet/findByStatus", params={'status' : 'sold'}, headers=header)
    #if api does not return success status
    if sold_pets_response.status_code != 200:
        print(f"unable to retrieve the data and status code is: {sold_pets_response.status_code}")
        return sold_pets_list
    #if api return success status
    else:
        sold_pets_json = sold_pets_response.json()
        for pet in sold_pets_json:
            pet_id = pet.get('id')
            pet_name = pet.get('name')
            sold_pets_list.append((pet_id, pet_name))
        return sold_pets_list

#calling function and storing in variable
sold_pets = sold_pets_func()

"""print("Sold pets in tuple format: ")
for i in sold_pets:
    print(i)"""