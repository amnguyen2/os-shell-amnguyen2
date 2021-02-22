import os, sys, re
from inout import myReadLine, writeLine
from myRedirect import redirOut, redirIn

def main():

    while True: # shell runs indefinitely
        if 'PS1' in os.environ:
            writeLine(os.environ['PS1'])
        else:
            writeLine("$ ")
            
        inputBuff = myReadLine()

        if len(inputBuff) > 0:
            inputHandler(inputBuff)


def inputHandler(inputBuff):
    if len(inputBuff) == 0:
        return
    
    if inputBuff == "exit": # user wants to exit shell loop
        writeLine("Exiting...\n")
        sys.exit(0)

    args = inputBuff.split(' ')
        
    if args[0] == "pwd": # PrintWorkingDirectory
        writeLine(os.getcwd() + "\n") # os.getcwd() returns CurrentWorkingDir

    elif args[0] == "cd": # ChangeDirectory
        try:
            if len(args) < 2: # no args for cd command
                return
            else:
                os.chdir(args[1])
        except:
            writeLine("cd %s: No such file or directory\n" % args[1])

    else:
        rc = os.fork() # os.fork() returns child's process ID

        if rc < 0: # fork failed
            os.write(2, ("Fork failed... returning %d\n" % rc).encode())
            sys.exit(1) # unsuccessful termination :(
        elif rc == 0:
            
            if '<' in args: # redir into indicator
                redirIn(args)
            
            elif '>' in args: # redir out to indicator
                redirOut(args)

            elif '|' in args: # pipe indicator
                pipeCmd(args)
                
            else:
                doCommand(args)
                sys.exit(0) # successful termination :)

            
def doCommand(args):
    for dir in re.split(":", os.environ["PATH"]): # try each directory in path
        program = "%s%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:                # ...expected
            pass                                 # ...fail quietly

    os.write(2, ("%s: could not execute\n" % args[0]).encode())
    sys.exit(1) # terminate with error

    
if __name__ == "__main__":
    main()
