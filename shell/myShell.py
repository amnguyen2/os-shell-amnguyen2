import os, sys, re
from inout import myReadLine, writeLine

def main():

    while True: # shell runs indefinitely
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())
            
        inputBuff = myReadLine()

        if len(inputBuff) > 0:
            inputHandler(inputBuff)
        """
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
        """

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
            if len(args) < 2:
                return
            else:
                os.chdir(args[1])
        except:
            writeLine("cd %s: No such file or directory\n" % args[1])
    else:
        rc = os.fork()

        if rc < 0:
            os.write(2, ("Fork failed... returning %d\n" % rc).encode())
            sys.exit(1) # unsuccessful termination :(
        elif rc == 0:
            doCommand(args)
            sys.exit(0) # successful termination :)
        else:
            os.wait()

                    
def doCommand(args):
    path = os.environ["PATH"]
    
    for dir in re.split(":", os.environ["PATH"]): # try each directory in path
        program = "%s%s" % (dir, args[0])

        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:                # ...expected
            pass                                 # ...fail quietly

    writeLine("%s: command not found\n" % args[0])
    sys.exit(1) # terminate with error

    
if __name__ == "__main__":
    main()
