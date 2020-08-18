import os
import subprocess
from timeit import default_timer as timer

class queiju:
    """
    pyQUEIJU: quantum espresso interface on jupyter.

    This library is a quantum espresso interface, but it is quite rudimentary.
    It takes as a parameter the input file for pw.x, bands.x, ... and runs
    the corresponding code on a single node.

    Properties
    ----------
    inp : string
        The input file
    out : string
        The output file
    files : string
        The list of new or modified files
    time : float
        Time it took to run the code, in seconds
    path: string
        Path for the QE binaries, if empty, assumes they are on $PATH
        
    Methods
    -------
    __init__(inp, path="")
        Class initialization
    run(cmd)
        Run the QE command cmd using the input file
        and save the output and list of modified files
    setpath(path)
        Defines the path where the QE binaries are located if not on $PATH
    saveoutput(file)
        Saves the output (out) into file
        
    """

    def __init__(self, inp, path=""):
        """
        Class initialization

        It takes the input parameters and initialize the object.

        Parameters
        ----------
        inp : string
            The input file

        """
        self.inp = inp  # init the input parameters for QE
        self.out = ""   # init the output file data as blank
        self.files = "" # init the list of modified files as blank
        self.time = 0   # init the time it took to run the code as 0
        self.path = ""  # init the QE binaries path
        self.setpath(path) # calls set path to check if binaries exist

    def saveoutput(self, file):
        try:
            print(self.out,  file=open(file, 'w'))
        except:
            raise Exception('pyQUEIJU: could not save output to file: ' + file)

    def setpath(self, newpath):
        """
        Sets the path for the QE binaries.

        Checks if the folder exists and contains the QE binaries. 
        If so, stores the new path.

        Parameters
        ----------
        cmd : string
            The QE command: [pw.x] [bands.x] [...]

        Returns
        -------
        float
            time it took to run, in seconds

        """
        # if blank, QE must be in $PATH
        if newpath == "":
            aux = subprocess.call(["which", "pw.x"])
            if aux != 0:
                raise Exception('pyQUEIJU: QE not found in PATH')
            else:
                self.path = ""
                return(0)
        
        # check if valid path
        if os.path.isdir(newpath) == False:
            raise Exception("pyQUEIJU: Invalid path: " + newpath)
        
        # if path is valid, make sure it ends with /
        if newpath[-1] != '/':
            newpath = newpath + '/'
            
        # if path is valid, check if binaries exist
        if os.path.isfile(newpath + "pw.x") == False:
            raise Exception("pyQUEIJU: QE binaries not found on " + newpath)
        
        # if all above is ok, use path
        self.path = newpath
        
    def run(self, cmd):
        """
        Run the QE command.

        Runs the desired QE command (cmd) and tracks the modified files and output data.

        Parameters
        ----------
        cmd : string
            The QE command: [pw.x] [bands.x] [...]

        Returns
        -------
        float
            time it took to run, in seconds

        """        

        # check if parameter is valid
        valid_cmds = ["pw.x", "bands.x"]
        if cmd not in valid_cmds:
            raise Exception('pyQUEIJU: invalid command '+str(cmd)+' on run')
        
        # check if binary is available
        if self.path == "":
            # check if binary exists on $PATH
            aux = subprocess.call(["which", cmd])
            if aux != 0:
                raise Exception("pyQUEIJU: Command not found on PATH:" + cmd)

        # if path != "", check if it is a folder
        elif os.path.isdir(self.path) == False:
            raise Exception("pyQUEIJU: Invalid path: " + self.path)
        
        # if path is valid, check if cmd exists within it
        elif os.path.isfile(self.path + cmd) == False:
            raise Exception("pyQUEIJU: Invalid command: " + self.path + cmd)

        # if reaches here, path+cmd must be a valid binary
        else:
            cmd = self.path + cmd
            
        # start the timer
        start = timer()
        # creates a file to help track file changes
        subprocess.run(["touch", ".lastwatch"])
        # run the cmd -inp pw.in > pw.out
        aux = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, input=self.inp)
        self.out = str(aux.stdout)
        # capture new or modified files 
        fnd = "find . -type f -cnewer .lastwatch"
        aux = subprocess.run(fnd.split(), text=True, stdout=subprocess.PIPE)
        self.files = str(aux.stdout)
        # stops the timer and save the time
        end = timer()
        self.time = end - start
        # all ok
        return(self.time)