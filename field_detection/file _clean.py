with open("recognized.txt") as stream:
    file = open("recognized_clean.txt", "a")
    for line in stream:
        # Empty lines will be ignored
        if line == "\n":
            pass
        else:
            file.write(line)
            # file.write('\n')
file.close