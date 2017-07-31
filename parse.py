import random
import os

note_names = [
    None,
    "a,,,", "ais,,,", "b,,,",
    "c,,", "cis,,", "d,,", "dis,,", "e,,", "f,,", "fis,,", "g,,", "gis,,", "a,,", "ais,,", "b,,",
    "c,", "cis,", "d,", "dis,", "e,", "f,", "fis,", "g,", "gis,", "a,", "ais,", "b,",
    "c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b",
    "c'", "cis'", "d'", "dis'", "e'", "f'", "fis'", "g'", "gis'", "a'", "ais'", "b'",
    "c''", "cis''", "d''", "dis''", "e''", "f''", "fis''", "g''", "gis''", "a''", "ais''", "b''",
    "c''',", "cis'''", "d'''", "dis'''", "e'''", "f'''", "fis'''", "g'''", "gis'''", "a'''", "ais'''", "b'''",
    "c''''", "cis''''", "d''''", "dis''''", "e''''", "f''''", "fis''''", "g''''", "gis''''", "a''''", "ais''''", "b''''",
    "c'''''"
]

def getnote(num):
    return note_names[int(num)]

def getnum(note):
    return note_names.index(note)

file = open("output_numbers.txt", "r")
lines = file.read().split("\n")[:-1]
file.close()

parts = []
for x in xrange(len(lines)):
    parts.append(lines[x].split(","))

parts2 = []
for x in xrange(len(parts)):
    line = []
    for y in xrange(len(parts[x])):
        line.append(getnote(parts[x][y]))
    parts2.append(line)

def separate(parts):
    retval = []

    for part in xrange(4):
        line = []
        for chord in parts:
            line.append(chord[part])
        retval.append(line)
    return retval

def addPassingTones(part):
    retval = []
    need4 = False

    for note in xrange(len(part) - 1):
        first, second = getnum(part[note]), getnum(part[note + 1])

        if abs(first - second) == 3:
            if random.random() < 0.5:
                retval.append("%s8" % (part[note]))
                if first > second:
                    retval.append("%s" % (getnote(getnum(part[note]) - 1)))
                else:
                    retval.append("%s" % (getnote(getnum(part[note]) + 1)))
                need4 = True
        else:
            if need4:
                retval.append("%s4" % (part[note]))
                need4 = False
            else:
                retval.append(part[note])
    if need4:
        retval.append("%s4" % (part[len(part) - 1]))
        need4 = False
    else:
        retval.append("%s" % (part[len(part) - 1]))
    return retval

def addEnding(parts):
    for x in xrange(4):
        if parts[x][len(parts[x]) - 1][-1] == "4" or parts[x][len(parts[x]) - 1][-1] == "8":
            parts[x][len(parts[x]) - 1] = parts[x][len(parts[x]) - 1][0:len(parts[x][len(parts[x]) - 1]) - 1]
        parts[x][len(parts[x]) - 1] = parts[x][len(parts[x]) - 1] + "1"
    return parts

parts = separate(parts2)
parts2 = []
parts2.append(parts[0])
parts2.append(parts[1])
parts2.append(parts[2])
parts2.append(parts[3])
# parts2.append(addPassingTones(parts[2]))
# parts2.append(addPassingTones(parts[3]))

parts = addEnding(parts2)
for part in parts:
    if part[0][len(part[0]) - 1] != "8" and part[0][len(part[0]) - 1]:
        part[0] = part[0] + "4"

def printout(parts):
    fh = open("output.ly", "w")
    fh.write("\\version \"2.12.1\"\n\n")

    def printvoice(voice):
        for note in voice:
            fh.write("%s " % (note))
        fh.write("} ")

    fh.write("\\header{\n")
    fh.write("\ttitle=\"Generated Music\"\n")
    fh.write("\tcomposer=\"Kevin Deisz\"\n")
    fh.write("}\n\n")

    fh.write("\\score {<<\n\t\\new Staff <<\n")
    fh.write("\t\t\\tempo 4=160\n")
    fh.write("\t\t\\clef treble\n\t\t{ ")
    printvoice(parts[3])

    fh.write("\\\\\n\t\t{ ")
    printvoice(parts[2])
    fh.write("\n\t>>\n")

    fh.write("\t\\new Staff <<\n")
    fh.write("\t\t\\tempo 4=160\n")
    fh.write("\t\t\\clef bass\n\t\t{ ")
    printvoice(parts[1])

    fh.write("\\\\\n\t\t{ ")
    printvoice(parts[0])
    fh.write("\n\t>>\n>>\n")

    fh.write("\t\\midi{ }\n")
    fh.write("\t\\layout{ }\n}\n")

    fh.close()
    os.system("bin/lilypond output.ly")

printout(parts)
