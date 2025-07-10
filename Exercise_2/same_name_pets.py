import requests

from Nestle.Exercise_2.Sold_pets import sold_pets_func

class SamePets:
    def __init__(self, pet_list):
        self.pet_list = pet_list

    def count_pet_name(self):
        temp_list = []
        for i in self.pet_list:
            temp_list.append(i[1])
        unique_list = list(set(temp_list))
        pet_dict = {}
        for i in unique_list:
            if i is None:
                continue
            count = 0
            for j in self.pet_list:
                if j[1] == i:
                    count += 1
            pet_dict[i] = count
        return pet_dict

sold_pets = sold_pets_func()
Counter = SamePets(sold_pets)
pet_name_count = Counter.count_pet_name()
print(pet_name_count)