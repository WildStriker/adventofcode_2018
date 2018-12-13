import re


def extract_claim(claim_line):
    match = re.match(
        '#[0-9]+ @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)',
        claim_line)

    return int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))


def count_overlaps(claims):
    dupe_check = {}
    total_overlap = 0
    for left, top, x_units, y_units in claims:
        fabric_pos_x = left
        for _ in range(x_units):
            fabric_pos_x += 1
            fabric_pos_y = top
            for _ in range(y_units):
                fabric_pos_y += 1
                coords = (fabric_pos_x, fabric_pos_y)

                count = dupe_check.get(coords, 0)
                count += 1
                dupe_check[coords] = count
                if count == 2:
                    total_overlap += 1

    return total_overlap


def main():
    with open('inputs\\input03.txt') as input_file:
        claims = map(extract_claim, input_file)

        total_overlap = count_overlaps(claims)

    print(total_overlap)


if __name__ == "__main__":
    main()
