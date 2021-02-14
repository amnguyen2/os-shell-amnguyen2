from os import read, write

inputBuff = None
strBuff = ""

def myReadLine():
    global strBuff

    while True: # read lines indefinitely
        currChar = myGetChar()

        if len(currChar) == 0: # empty string
            return currChar

        if currChar == '\n': # end of line
            line = strBuff
            strBuff = ""
            return line
        else: 
            strBuff = strBuff + currChar # add to strBuff
        

def myGetChar():
    global inputBuff
    global strBuff

    if inputBuff == None or len(strBuff) == 0:
        inputBuff = read(0, 100)
        strBuff = inputBuff.decode()

    if len(strBuff) > 0:
        firstChar = strBuff[0]
        strBuff = strBuff[1:]
        return firstChar
    else:
        return strBuff

def writeLine(line):
    write(1, line.encode())
