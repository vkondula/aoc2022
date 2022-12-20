def seek(seq, index):
    for current_index, record in enumerate(seq):
        (value, or_index) = record
        if or_index == index:
            return value, current_index
    raise KeyError


if __name__ == '__main__':
    with open("inputs/20.txt", "r") as f:
        original = [int(value.strip("\n")) for value in f.readlines()]
    m = len(original)
    working = [(value, i) for i, value in enumerate(original.copy())]
    for original_index in range(m):
        value, i = seek(working, original_index)
        working.pop(i)
        new_i = (i + value) % (m - 1)
        working.insert(new_i, (value, original_index))
    zero_i = [i for i, record in enumerate(working) if record[0] == 0][0]
    found = [working[(zero_i + i * 1000) % m] for i in range(1, 4)]
    print(sum(value for value, _ in found))
