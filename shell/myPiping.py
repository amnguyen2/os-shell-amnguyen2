import os, sys

def pipeCmd(args):
    left = args[0:args.index("|")]
    right = args[args.index("|") + 1:]

    pr, pw = os.pipe() # pipe read, pipe write
    rc = os.fork() 

    if rc < 0: # fork failure
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        system.exit(1)

    elif rc == 0:
        os.close(1) # close output fd
        os.dup(pw) # os.dup(fd) duplicate file descriptor
        os.set_inheritable(1, True) # accessibility

        for fd in (pr, pw): # from pr to pw
            os.close(fd) # close this fd
        execute_cmd(left)
        os.write(2, ("Could not execute :(").encode())
        sys.exit(1)

    else:
        os.close(0) # keyboard (fd 0)
        os.dup(pr) # duplicate pipe read fd
        os.set_inheritable(0, True)
        
        for fd in (pw, pr): # from pw to pr
            os.close(fd)
            
        if "|" in right: 
            pipeCmd(right) # continue recursively

        execute_cmd(right)
        os.write(2, ("Could not execute :("). encode())
        sys.exit(1)
            

def execute_cmd(args):
    for dir in re.split(":", os.environ["PATH"]):
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, ("%s : command not found\n" % (args[0])).encode())
    sys.exit(1)
