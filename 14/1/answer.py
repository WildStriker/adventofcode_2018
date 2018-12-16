def main():

    with open('inputs\\input14.txt') as input_file:
        recipe_count = int(input_file.read())

    elves = [0, 1]
    new_recipe_count = 10
    recipes = [3, 7]
    while len(recipes) < new_recipe_count + recipe_count:
        new_recipes = 0
        for index, recipe_index in enumerate(elves):
            score = recipes[recipe_index]
            new_recipes += score
            elves[index] = elves[index] + score + 1

        for number in str(new_recipes):
            recipes.append(int(number))

        for index, _ in enumerate(elves):
            elves[index] %= len(recipes)

    output = map(str, recipes[recipe_count:recipe_count + new_recipe_count])
    output = ''.join(output)
    print(output)


if __name__ == "__main__":
    main()
