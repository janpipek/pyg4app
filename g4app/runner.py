import tempfile
import subprocess
import signal
import os
import sys

G4APP_PATH = os.getenv("G4APP_PATH") or "."
G4APP_NAME = os.getenv("G4APP_NAME") or "g4"


def kill(_signal, _frame):
    '''A special method to be substituted for default interrupt signal handling.

    It passes interrupt signal to the executed process.'''
    global g4process
    g4process.terminate()
    g4process = None
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def execute(macro, macro_path=None, delete_macro_file=True, valgrind=False, gdb=False):
    '''Create a temporary file from the commands and run it.

    :param macro: A Macro to write and execute.
    :param macro_path: A path where the macro file should be written.
        If not set, a temporary file will be created.
    :param delete_macro_file: If set, delete macro file after execution.
    :param valgrind: Run the application in valgrind for debugging.
    :param gdb: Run the application in gdb for debugging.
    '''
    global g4process

    # TODO: Make cwd and application name configurable
    # TODO: Ensure all paths are treated well (Escape them)
    if macro_path:
        f = open(macro_path, "w")
    else:
        f = tempfile.NamedTemporaryFile(suffix=".mac", delete=False)
        macro_path = f.name
    # TODO: Change to real logging
    print "Writing macro to {}".format( macro_path )
    print
    print "*" * 80
    macro.write(sys.stdout)
    print "*" * 80

    print
    sys.stdout.flush()
    macro.write(f)
    f.close()
    signal.signal(signal.SIGINT, kill) # Bubble interruption to subprocess (and kill it)
    if valgrind:
        g4process = subprocess.Popen(["valgrind", "./" + G4APP_NAME, macro_path], cwd=G4APP_PATH)
    elif gdb:
        g4process = subprocess.Popen(["gdb", "./" + G4APP_NAME, "-ex", "run {}".format(macro_path)], cwd=G4APP_PATH)
    else:
        g4process = subprocess.Popen(["./" + G4APP_NAME, macro_path], cwd=G4APP_PATH)
    g4process.wait()
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Restore default interruption behaviour
    if delete_macro_file:
        os.remove( macro_path )