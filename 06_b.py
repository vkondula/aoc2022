if __name__ == '__main__':
    with open("inputs/6.txt", "r") as f:
        data_in = f.read()
    for index in range(3, len(data_in)):
        if len(set(data_in[index - 14: index])) == 14:
            print(index)
            break
