with open("thefile.txt", "r") as inf:
    with open("wikipedia.txt", "w") as fixed:
        for line in inf:
            fixed.write(line)