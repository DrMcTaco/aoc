from collections import defaultdict

from aocd import get_data
from dotenv import load_dotenv


load_dotenv()

t = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def parse_foods(input: str):
    foods = []
    all_components, all_allergens = set(), defaultdict(set)
    for food in input.splitlines():
        components, alergens = food.split(" (contains ")
        all_components |= set(components)
        alergens = alergens.strip(")").split(", ")
        components = components.split()
        for alergen in alergens:
            all_allergens[alergen] |= set(components)
        foods += [(set(components), set(alergens))]
    return foods, all_components, all_allergens

def finalize(allergens, allergen):
    for target in allergens:
        if target != allergen and len(allergens[target]) != 1:
            allergens[target] -= allergens[allergen]
            if len(allergens[target]) == 1:
                finalize(allergens, target)

if __name__ == "__main__":
    input = get_data(day=21, year=2020)
    foods, components, allergens = parse_foods(input)
    probable = {}
    for allergen in allergens:
        for food in foods:
            if allergen in food[1]:
                allergens[allergen] &= set(food[0])
            if len(allergens[allergen]) == 1:
                finalize(allergens, allergen)

    count = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient not in [allergen for types in allergens.values() for allergen in types]:
                count +=1
    print(count)
    print(allergens)
    cannonical = []
    for allergen, ingredient in allergens.items():
        cannonical += [(allergen, ingredient.copy().pop())]

    cannonical.sort()
    print(",".join([ingredient[1] for ingredient in cannonical]))
