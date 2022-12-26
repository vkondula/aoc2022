def to_snafu(number):
    if number == 0:
        return 0
    nums = []
    while number:
        number, rem = divmod(number, 5)
        nums.append(rem)
    nums.append(0)
    retval = list(reversed(nums))
    while any(value > 2 or value < -2 for value in retval):
        for i, value in enumerate(retval):
            if value > 2:
                retval[i - 1] += 1
                retval[i] -= 5
            if value < -2:
                retval[i - 1] -= 1
                retval[i] += 5
    dump_retval = [
        str(value).replace("-1", "-").replace("-2", "=")
        for value in retval
    ]
    return "".join(dump_retval).lstrip("0")


def main():
    with open("inputs/25.txt", "r") as f:
        data_in = f.readlines()
    total_sum = 0
    for line in data_in:
        line_sum = 0
        for i, value in enumerate(reversed(line.strip("\n"))):
            tmp = int(value.replace("-", "-1").replace("=", "-2"))
            line_sum += (5 ** i) * tmp
        total_sum += line_sum
    print(total_sum)
    print(to_snafu(total_sum))

if __name__ == '__main__':
    main()
