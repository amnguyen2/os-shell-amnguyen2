import os, re

def redirOut(args):
    os.close(1) # display was set to fd 1

    out_indicate = args.index('>')+1
    
    os.open(args[out_indicate], os.O_WRONLY | os.O_CREAT) # out file
    os.set_inheritable(1, True)

    args.remove(args[out_indicate]) # remove argument from args, no use anymore
    args.remove('>') # remove output indicator from command line args

    execute_redir(args)


def redirIn(args):
    os.close(0) # keyboard was set to fd 0

    in_indicate = args.index('<')+1

    os.open(args[in_indicate], os.O_RDONLY) # in file 
    os.set_inheritable(0, True) 

    args.remove(args[in_indicate]) # remove arg from args, no use anymor
    args.remove('<') # remove input indicator from command line args
    
    execute_redir(args)


def execute_redir(args):
    for dir in re.split(":", os.environ["PATH"]): # try each dir in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError: # ... expected
            pass # ... fail quietly

        
