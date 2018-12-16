def main():

    with open('inputs\\input14.txt') as input_file:
        patterns = []
        for recipe_pattern in input_file.read():
            patterns.append(recipe_pattern)

    elves = [0, 1]
    recipes = [3, 7]
    pattern_index = 0
    while True:
        new_recipes = 0
        for index, recipe_index in enumerate(elves):
            score = recipes[recipe_index]
            new_recipes += score
            elves[index] = elves[index] + score + 1

        for number in str(new_recipes):
            recipes.append(int(number))
            if number != patterns[pattern_index]:
                pattern_index = 0

            if number == patterns[pattern_index]:
                pattern_index += 1
                if pattern_index == len(patterns):
                    length = len(recipes) - len(patterns)
                    print(length)
                    return

        for index, _ in enumerate(elves):
            elves[index] %= len(recipes)


if __name__ == "__main__":
    main()
