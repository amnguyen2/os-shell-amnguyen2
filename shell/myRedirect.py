import os

def redirOut(args):
    os.close(1) # display was set to fd 1

    out_indicate = args.index('>')
    
    os.open(args[out_indicate], os.O_WRONLY | os.O_CREAT) # out file
    os.set_inheritable(1, True)

    args.remove(args[out_indicate+1]) # remove argument from args, no use anymore
    cmd = args[out_indicate-1] # get command
    args.remove('>') # remove output indicator from command line args
    args.remove(args[0])

def redirIn(args):
    os.close(0) # keyboard was set to fd 0

    in_indicate = args.index('<')

    os.open(args[in_indicate], os.RDONLY) # in file 
    os.set_inheritable(0, True) 

    args.remove(args[in_indicate+1]) # remove arg from args, no use anymore
    cmd = args[in_indicate-1] # get command
    args.remove('<') # remove input indicator from command line args
    args.remove(args[0])
