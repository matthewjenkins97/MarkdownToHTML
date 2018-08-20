import sys


def markdownpass(file):
    print(file)
    # from here we look through each line and check the beginning of each line
    # if it starts with a certain symbol we take everything after the line start and shove it into the proper html

    # but how would we do stuff inside each line?


def main():
    # check whether the argv is 2 elements long - if it isn't we crash
    if len(sys.argv) != 2:
        print("USAGE: markdowntohtml.py file.md")
        quit(1)
    # get filename - if last 3 chars aren't .md we crash
    filename = sys.argv[1].lower()
    if filename[-3:] != ".md":
        print("USAGE: markdowntohtml.py file.md")
        print("File must be a .md file.")
        quit(1)
    # get file from sys.argv[1] and take every line and put it into a list
    # if file doesn't exist, we crash.
    try:
        file = open("./" + sys.argv[1])
    except IOError:
        print("USAGE: markdowntohtml.py file.md")
        print("File does not exist.")
        quit(1)
    # convert file to array and chomp any newlines
    filelines = []
    for line in file:
        filelines.append(line.strip('\n'))
    markdownpass(filelines)


main()
