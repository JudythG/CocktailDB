# Class project to read data from an API.
# Reads 1000 random drinks from The Cocktail DB
# Counts drinks by type: is alcoholic, optional alcohol, non-alcoholic
# Counts ingredients per drink
# Outputs frequency for drink type and ingredients

import requests
#import operator
import csv

def get_drink_type(drink, alcohol_counter):
    drink_type = drink['strAlcoholic']
    if drink_type in alcohol_counter.keys():
        alcohol_counter[drink_type] += 1
    else:
        alcohol_counter[drink_type] = 1

def main():
    alcohol_counter = {}
    ingredients = {}

    counter = range(0,1000)
    for c in counter:
        req = requests.get ("https://www.thecocktaildb.com/api/json/v1/1/random.php")
        if int(req.status_code) == 200:
            drinks = req.json()['drinks']
            for drink in drinks:

                # is drink alcoholic or not?
                get_drink_type (drink, alcohol_counter)

                # ingredients
                for drink_key in drink.keys():
                    if drink_key.startswith ('strIngredient'):
                        ingredient = drink[drink_key]
                        if ingredient in ingredients.keys():
                            ingredients[ingredient] += 1
                        else:
                            ingredients[ingredient] = 1

    with open ('is_alcoholic.csv', 'w', newline='') as csvfile:
        fieldnames = ['Drink Type', 'Frequency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for type, count in alcohol_counter.items():
            if type:
                writer.writerow({'Drink Type': type, 'Frequency': count})


    with open ('ingredients.csv', 'w', newline='') as csvfile:
        fieldnames = ['Ingredient', 'Frequency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        ctr = 0
        sorted_ingredients = sorted (ingredients.items(), key=lambda kv: kv[1], reverse=True)
        for d in sorted_ingredients:
            ingredient = d[0]
            count = d[1]
            if ingredient:
                ctr += 1
                if (ctr > 25 ):
                    break
                writer.writerow({'Ingredient':ingredient, 'Frequency': count})

# main
main ()

