import glob
import os
import sys
import random
import re

#count the lines in the file
def countLines(f):
    i = 0
    for line in f:
        if line.strip():
            i += 1
    return i

#randomly create a syntactically valid line
def generateLine(lines):
    instruction = random.choice(['Sense', 'Mark', 'Unmark', 'PickUp', 'Drop', 'Turn', 'Move', 'Flip'])
    senseDir = random.choice(['Here', 'Ahead', 'LeftAhead', 'RightAhead'])
    conditionMarkInt = random.randint(0, 5)
    condition = random.choice(['Friend', 'Foe', 'FriendWithFood', 'Food', 'Rock', 'Marker', 'FoeMarker', 'Home', 'FoeHome'])
    if (condition == 'Marker'):
        condition += ' ' + str(conditionMarkInt)
    markInt = random.randint(0, 5)
    turnDir = random.choice(['Left', 'Right'])
    st1 = random.randint(0, lines)
    st2 = random.randint(0, lines)
    flipP = 2
    return {
            'Sense' : ' '.join([instruction, senseDir, str(st1), str(st2), condition]),
            'Mark' : ' '.join([instruction, str(markInt), str(st1)]),
            'Unmark' : ' '.join([instruction, str(markInt), str(st1)]),
            'PickUp' : ' '.join([instruction, str(st1), str(st2)]),
            'Drop' : ' '.join([instruction, str(st1)]),
            'Turn' : ' '.join([instruction, turnDir, str(st1)]),
            'Move' : ' '.join([instruction, str(st1), str(st2)]),
            'Flip' : ' '.join([instruction, str(flipP), str(st1), str(st2)]),
            }[instruction]



#mutate the file, ie examine ever instruction and with certain probabilities add a line at the current position or at the end of the file, or delete the current line
def mutateFile(f, lines):
    appendLine = 0.01
    insertLine = 0.01
    deleteLine = 0.0012
    ResultStr = ''
    AppendStr = ''
    i = 0
    for line in f:
        i += 1
        randFloat = random.random()
        if randFloat < appendLine:
            ResultStr += line
            AppendStr += generateLine(lines) + "\n"
        elif randFloat < appendLine + insertLine:
            ResultStr += line
            ResultStr += generateLine(lines) + "\n"
        #if don't delete line, ie randFloat skips deleteLine, then just do default and don't mutate
        elif randFloat > appendLine + insertLine + deleteLine:
            ResultStr += line
        else:
            ResultStr += 'Flip 3 ' + str(i%lines) + ' ' + str(i%lines) + '\n'
    ResultStr += AppendStr
    return ResultStr

#create a function for the re.sub call in fixLengths to change states to the approriate length of the file
def replaceStringGenerator(lines):
    return lambda integer: integer.group(1) + str(int(integer.group(2)) % lines) + integer.group(3)

#fix the state references so that if any thing references a line that is beyond what is now the end of the file, fix that state reference.
def fixLengths(f, lines):
    InputStr = ''
    for line in f:
        InputStr += line
    return re.sub('(\s)(\d+)(\s)', replaceStringGenerator(lines), InputStr)

#call a function that takes a filename and a file length on every file in the directory
def fileCountAndFunc(fname, fileFunc):
    # Open a file twice, once to count number of lines and next to mutate it
    fileLines = open(fname, "r+")
    f = open(fname, "r+")
    newFileStr = fileFunc(f, countLines(fileLines))
    f.seek(0)
    f.write(newFileStr)
    f.truncate()
    f.close()
    fileLines.close()

#mutate all of the files in the given directory
def mutateDirectory():
    for fname in os.listdir("."):
        fileCountAndFunc(fname, mutateFile)
        #fileCountAndFunc(fname, fixLengths)

def main():
    if len(sys.argv) != 3:
        print "Need the directory to mutate and then the number of generations"
    os.chdir(sys.argv[1])
    for i in range(int(sys.argv[2])):
        mutateDirectory()

if __name__ == "__main__":
    main()
