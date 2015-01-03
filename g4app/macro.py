class Macro(object):
    '''A collection of macro commands.'''

    def __init__(self, path = None):
        '''Constructor.

        :param path: a path to macro file that will be included at the beginning.'''
        self.commands = []
        if path:
            self.include(path)

    def add(self, command):
        '''Add a command.

        What can be included:
        * a string
        * an object with "render" method that should return a list of strings
        * a list of any of the previous
        * a false-like object (does nothing)

        Note: the render method is called at the time of addition.
        '''
        if not command:
            return # Do nothing
        elif isinstance(command, list):
            for cmd in command:
                self.add(cmd)
        elif hasattr(command, "render"):
            for command in command.render():
                self.add(command)
        else:
            command = command.strip()
            if len(command):
                self.commands.append(command)

    def __add__(self, command):
        m = self.clone()
        m.add(command)
        return m

    def include(self, file_path):
        '''Include all macro commands from a text file.

        Lines starting with # are considered to be comments.
        '''
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if len(line) and line[0] != "#":
                    self.add( line )

    def write(self, f):
        '''Write all commands to a file.

        :param f: can be either a file-like object or a path.
        '''
        if isinstance(f, basestring):
            with open(file, "w") as f:
                self.write(f)
        else:
            for command in self.commands:
                f.write(command + "\n")

    def clone(self):
        '''Create an identical copy of this macro.
        '''
        new = Macro()
        new.commands = self.commands[:] 
        return new


class MacroBuilder(object):
    '''A simple container of macro commands.

    Useful to be inherited from.'''
    def __init__(self, commands=()):
        self._commands = list(commands)

    def render(self):
        return self._commands