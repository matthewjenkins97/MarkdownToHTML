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


def markdownpass(file, filename):
    """goes through each line and check each line for appropriate markdown
    elements using regex """

    # converting filename to an html file and dumping a boilerplate into it

    html_file = open(filename[:-3] + ".html", "w")
    html_file.write(boilerplate)

    for line in file:

        # setting specific flags
        bolded = False
        italicized = False
        no_match = True

        # headings
        match = re.match("(#{1,6})(.*)", line)
        if match:
            # once you see a heading, we replace the front of the text with the
            # proper tag, put the text after the heading into a string, and
            # then end it with the proper tag
            temp_line = "<h" + str(len(match.group(1))) + ">" + \
                        str(match.group(2)) + "</h" + \
                        str(len(match.group(1))) + ">"
            html_file.write(temp_line)
            no_match = False

        # bold, italics, unordered lists
        # these are all being checked en masse because of the common symbol *

        # bold
        match = re.search("\*{2}(.*)\*{2}", line)
        if match:
            temp_line = "<b>" + str(match.group(1)) + "</b>"
            html_file.write(temp_line)
            bolded = True
            no_match = False

        # italics
        match = re.search("\*(.*)[^\\\\]\*", line)
        if match and not bolded:
            temp_line = "<em>" + str(match.group(1)) + "</em>"
            html_file.write(temp_line)
            italicized = True
            no_match = False

        # unordered lists
        match = re.search("^\*(.*)", line)
        if match and not bolded and not italicized:
            temp_line = "<ul><li>" + str(match.group(1)) + "</li></ul>"
            html_file.write(temp_line)
            no_match = False

        # miscellany
        # quoted text
        match = re.search("^>(.*)", line)
        if match:
            temp_line = "<blockquote>" + str(match.group(1)) + "</blockquote>"
            html_file.write(temp_line)
            no_match = False

        # links
        match = re.search("\[(.*)\]\((.*)\)", line)
        if match:
            temp_line = "<a href=" + str(match.group(2)) + ">" + \
                        str(match.group(1)) + "</a>"
            html_file.write(temp_line)
            no_match = False

        # strikethrough text
        match = re.search("~~(.*)~~", line)
        if match:
            temp_line = "<s>" + str(match.group(1)) + "</s>"
            html_file.write(temp_line)
            no_match = False

        # superscript
        match = re.search("^\^(.*)", line)
        if match:
            temp_line = "<sup>" + str(match.group(1)) + "</sup>"
            html_file.write(temp_line)
            no_match = False

        # escape sequences
        # these will be simple find and replaces
        # asterisk *
        match = re.search("\\\\\*", line)
        if match:
            html_file.write("*")
            no_match = False

        # greater than >
        match = re.search("\\\\>", line)
        if match:
            html_file.write(">")
            no_match = False

        # hashtag #
        match = re.search("\\\\#", line)
        if match:
            html_file.write("#")
            no_match = False

        # tilde ~
        match = re.search("\\\\~", line)
        if match:
            html_file.write("~")
            no_match = False

        # parens ()
        match = re.search("\\\\\(", line)
        if match:
            html_file.write("(")
            no_match = False
        match = re.search("\\\\\)", line)
        if match:
            html_file.write(")")
            no_match = False

        # parens {}
        match = re.search("\\\\\{", line)
        if match:
            html_file.write("{")
            no_match = False
        match = re.search("\\\\\}", line)
        if match:
            html_file.write("}")
            no_match = False

        # parens []
        match = re.search("\\\\\[", line)
        if match:
            html_file.write("[")
            no_match = False
        match = re.search("\\\\\]", line)
        if match:
            html_file.write("]")
            no_match = False

        # caret ^
        match = re.search("\\\\\^", line)
        if match:
            html_file.write("^")
            no_match = False

        # backslashes \
        # this has to be some sort of joke...
        match = re.search("\\\\{2}", line)
        if match:
            html_file.write("\\")
            no_match = False

        # if line is empty place a linebreak
        if line == "":
            html_file.write("<br>")

        # if the line doesn't contain any match we just print it as is
        if no_match:
            html_file.write(line)

        # wrap up this line with a \n (mostly for neatness in the html file)
        html_file.write("\n")

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
