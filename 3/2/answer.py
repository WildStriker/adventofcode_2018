import re


def extract_claim(claim_line):
    match = re.match(
        '#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)',
        claim_line)

    return match.group(1), int(match.group(2)), \
        int(match.group(3)), int(match.group(4)), int(match.group(5))


def no_overlaps(claims):
    no_dupe_claims = set()
    dupe_check = {}
    for claim, left, top, x_units, y_units in claims:
        is_overlapped = False
        fabric_pos_x = left
        for _ in range(x_units):
            fabric_pos_x += 1
            fabric_pos_y = top
            for _ in range(y_units):
                fabric_pos_y += 1
                coords = (fabric_pos_x, fabric_pos_y)

                last_claim = dupe_check.get(coords, None)
                dupe_check[coords] = claim
                if last_claim:
                    is_overlapped = True
                    if last_claim in no_dupe_claims:
                        no_dupe_claims.remove(last_claim)

        if not is_overlapped:
            no_dupe_claims.add(claim)

    return no_dupe_claims


def main():
    with open('inputs\\input03.txt') as input_file:
        claims = map(extract_claim, input_file)

        claim_overlap_free = no_overlaps(claims)

    print(claim_overlap_free)


if __name__ == "__main__":
    main()
