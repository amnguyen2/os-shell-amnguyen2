import os, sys, time, re
from inout import myReadLine, writeLine

def main():

    while True: # shell runs indefinitely
        writeLine("< ")
        inputLine = myReadLine()

        if inputLine == "exit" or inputLine == "x":
            break # leave loop, stop shell

        args = inputLine.split(" ") # args is list of words

        rc = os.fork() # rc = return child

        if rc < 0:
            writeLine("Child fork fell on its face :(")
            sys.exit(1)
        elif rc == 0:
            writeLine("Trying to complete commands...")
            doCommand(args)
            sys.exit(1)
        else:
            os.wait()


def doCommand(args):
    path = os.environ["PATH"]

    for dir in re.split(":", os.environ["PATH"]): # try each directory in path
        program = "%s%s" % (dir, args[0])

        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:
            pass

    writeLine("Command fell on its face :(\n")
    sys.exit(1)

if __name__ == "__main__":
    main()
