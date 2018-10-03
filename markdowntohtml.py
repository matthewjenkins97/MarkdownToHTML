#!/usr/local/bin/python3

import sys
import re


def markdownpass(file):
    """goes through each line and check each line for appropriate markdown
    elements using regex """

    for line in file:
        print(line)

        # headings
        match = re.match("(#{1,6})(.*)", line)
        if match:
            # once you see a heading, we replace the front of the text with the
            # proper tag, put the text after the heading into a string, and
            # then end it with the proper tag
            print("Header " + str(len(match.group(1))) + " found")

        # bold, italics, unordered lists
        # these are all being checked en masse because of the common symbol *

        # bold
        if re.search("\*{2}(.*)\*{2}", line) is not None:
            print("Bold found")

        # italics
        elif re.search("\*(.*)\*", line) is not None:
            print("Italics found")

        # unordered lists
        elif re.search("[^\\\\]\*(.*)", line) is not None:
            print("Unordered list found")

        # miscellany
        # quoted text
        if re.search(">+\s+(.*)", line) is not None:
            print("Quoted text found")

        # links
        if re.search("\[(.*)\]\((.*)\)", line) is not None:
            print("Links found")

        # strikethrough text
        if re.search("~~(.*)~~", line) is not None:
            print("Strikethrough found")

        # superscript
        if re.search("\s*^\^(.*)", line) is not None:
            print("Superscript found")

        # escape sequences
        # these will be simple find and replaces

        # asterisk *
        if re.search("\\\\\*", line) is not None:
            print("* found")

        # greater than >
        if re.search("\\\\>", line) is not None:
            print("> found")

        # hashtag #
        if re.search("\\\\#", line) is not None:
            print("# found")

        # tilde ~
        if re.search("\\\\~", line) is not None:
            print("~ found")

        # parens ()
        if re.search("\\\\\(", line) is not None:
            print("( found")
        if re.search("\\\\\)", line) is not None:
            print(") found")

        # parens {}
        if re.search("\\\\\{", line) is not None:
            print("{ found")
        if re.search("\\\\\}", line) is not None:
            print("} found")

        # parens []
        if re.search("\\\\\[", line) is not None:
            print("{ found")
        if re.search("\\\\\]", line) is not None:
            print("} found")

        # caret ^
        if re.search("\\\\\^", line) is not None:
            print("^ found")

        # backslashes \
        # this has to be some sort of joke...
        if re.search("\\\\{2}", line) is not None:
            print("\\ found")


def main():
    """makes sure the sys.argv and sys.argc are consistent with the desires
    of any function call"""

    # check whether the argv is 2 elements long - if it isn't we crash
    if len(sys.argv) != 2:
        print("USAGE: markdowntohtml.py file.md")
        quit(1)

    # get filename - if last 3 chars aren't .md we crash
    filename = sys.argv[1].lower()
    if filename[-3:].lower() != ".md":
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

    # run the markdown to html conversion algorithm
    markdownpass(filelines)


main()
