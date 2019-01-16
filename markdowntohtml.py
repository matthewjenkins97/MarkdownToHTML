#!/usr/local/bin/python3

import sys
import re

boilerplate = """<!DOCTYPE html>
<html>
<body>
"""

end = """
</body>
</html>
"""


def conversion(line, html_file):
    """building an html line from bottom up using recursion"""

    # print(line)

    # escape sequences
    # these will be simple find and replaces
    # asterisk *
    match = re.search("(.*)\\\\\*(.*)", line)
    if match:
        return match.group(1) + "*" + match.group(2)

    # greater than >
    match = re.search("(.*)\\\\>(.*)", line)
    if match:
        return match.group(1) + ">" + match.group(2)

    # hashtag #
    match = re.search("(.*)\\\\#(.*)", line)
    if match:
        return match.group(1) + "#" + match.group(2)

    # tilde ~
    match = re.search("(.*)\\\\~(.*)", line)
    if match:
        return match.group(1) + "~" + match.group(2)

    # parens ()
    match = re.search("(.*)\\\\\((.*)", line)
    if match:
        return match.group(1) + "(" + match.group(2)
    match = re.search("(.*)\\\\\)(.*)", line)
    if match:
        return match.group(1) + ")" + match.group(2)

    # parens {}
    match = re.search("(.*)\\\\\{(.*)", line)
    if match:
        return match.group(1) + "{" + match.group(2)
    match = re.search("(.*)\\\\\}(.*)", line)
    if match:
        return match.group(1) + "}" + match.group(2)

    # parens []
    match = re.search("(.*)\\\\\[(.*)", line)
    if match:
        return match.group(1) + "[" + match.group(2)
    match = re.search("(.*)\\\\\](.*)", line)
    if match:
        return match.group(1) + "]" + match.group(2)

    # caret ^
    match = re.search("(.*)\\\\\^(.*)", line)
    if match:
        return match.group(1) + "^" + match.group(2)

    # backslashes \
    # this has to be some sort of joke...
    match = re.search("(.*)\\\\{2}(.*)", line)
    if match:
        return match.group(1) + "\\" + match.group(2)

    # headings
    match = re.match("(#{1,6})(.*)", line)
    if match:
        # once you see a heading, we replace the front of the text with the
        # proper tag, put the text after the heading into a string, and
        # then end it with the proper tag
        # print("Heading found")
        return "<h" + str(len(match.group(1))) + ">" + \
               conversion(match.group(2), html_file) + "</h" + \
               str(len(match.group(1))) + ">"

    # bold, italics, unordered lists
    # these are all being checked en masse because of the common symbol *

    # unordered lists
    match = re.search("^\* (.*)", line)
    if match:
        # print("Unordered list found")
        # print("Match: " + str(match.group(1)))
        return "<ul><li>" + conversion(match.group(1), html_file) + \
               "</li></ul>"

    # bold
    match = re.search("(.*)\*{2}(.*)\*{2}(.*)", line)
    if match:
        # print("Bold found")
        return conversion(match.group(1), html_file) + "<b>" + \
            conversion(match.group(2), html_file) + "</b>" + \
            conversion(match.group(3), html_file)

    # italics
    match = re.search("(.*)\*(.*)\*(.*)", line)
    if match:
        # print("Italics found")
        return conversion(match.group(1), html_file) + "<em>" + \
            conversion(match.group(2), html_file) + "</em>" + \
            conversion(match.group(3), html_file)

    # miscellany
    # quoted text
    match = re.search("^> (.*)", line)
    if match:
        # print("Blockquote found")
        return "<blockquote>" + \
               conversion(match.group(1), html_file) + "</blockquote>"

    # links
    match = re.search("(.*)\[(.*)\]\((.*)\)(.*)", line)
    if match:
        # print("Links found")
        return conversion(match.group(1), html_file) + "<a href=" + \
            conversion(match.group(3), html_file) + ">" + \
            conversion(match.group(2), html_file) + "</a>" + \
            conversion(match.group(4), html_file)

    # strikethrough text
    match = re.search("~~(.*)~~", line)
    if match:
        # print("Strikethrough found")
        return "<s>" + conversion(match.group(1), html_file) + "</s>"

    # superscript
    match = re.search("^\^(.*)", line)
    if match:
        # print("Superscript found")
        return"<sup>" + conversion(match.group(1), html_file) + "</sup>"

    # if the line doesn't contain any match we just print it as is
    # print("Nothing found")
    return line


def markdownpass(file, filename):
    """goes through each line and check each line for appropriate markdown
    elements using regex """

    # converting filename to an html file and dumping a boilerplate into it

    html_file = open(filename[:-3] + ".html", "w")
    html_file.write(boilerplate)

    # goes through every line in the file
    for line in file:
        # if line is empty, place a linebreak and continue
        if line == "":
            html_file.write("<br>")
        else:
            # otherwise, run a conversion algorithm on the line
            html_file.write(conversion(line, html_file))
        # wrap up this line with a \n (mostly for neatness in the html file)
        html_file.write("\n")
        # print()

    html_file.write(end)


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
    markdownpass(filelines, sys.argv[1])


main()
