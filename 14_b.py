if __name__ == '__main__':
    with open("inputs/14.txt", "r") as f:
        data_in = f.readlines()
    occupied = set()
    for raw_row in data_in:
        records = [[int(record.split(",")[0]), int(record.split(",")[1])] for record in raw_row.strip("\n").split(" -> ")]
        for i, record in enumerate(records):
            if i == 0:
                continue
            min_x, max_x = min(record[0], records[i-1][0]), max(record[0], records[i-1][0]) + 1
            min_y, max_y = min(record[1], records[i - 1][1]), max(record[1], records[i - 1][1]) + 1
            for x in range(min_x, max_x):
                for y in range(min_y, max_y):
                    occupied.add((x, y))
    end_y = max(occupied, key=lambda x: x[1])[1] + 1
    sand_count = 0
    found = False
    while not found:
        sand = (500, 0)
        next_sand = (500, 0)
        while True:
            if sand[1] == end_y:
                occupied.add(sand)
                sand_count += 1
                break
            if (next_sand := (sand[0], sand[1] + 1)) not in occupied:
                sand = next_sand
                continue
            if (next_sand := (sand[0] - 1, sand[1] + 1)) not in occupied:
                sand = next_sand
                continue
            if (next_sand := (sand[0] + 1, sand[1] + 1)) not in occupied:
                sand = next_sand
                continue
            if not(sand[1]):
                found = True
                sand_count += 1
                break
            occupied.add(sand)
            sand_count += 1
            break
    print(sand_count)
