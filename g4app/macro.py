class Macro(object):
    '''A collection of macro commands.'''

    def __init__(self, path = None):
        '''Constructor.

        :param path: a path to macro file that will be included at the beginning.'''
        self.commands = []
        if path:
            self.include(path)

    def add(self, command):
        self.commands.append(command)
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

    @property
    def commands(self):
        return self._commands

    def add_command(self, command):
        self._commands.append(command)

    def render(self):
        """All command lines (generator function)."""
        for command in self.commands:
            # 1. ignore false-like objects
            if not command:
                continue

            # 2. create iterator walking down the tree
            if hasattr(command, "render"):
                iterator = command.render()
            elif isinstance(command, basestring):
                iterator = (command,)
            elif hasattr(command, "__iter__"):
                builder = MacroBuilder(command)
                iterator = builder.render()

            # 3. get all lines from the iterator
            for line in iterator:
                yield line


class WrappedMacroBuilder(MacroBuilder):
    def __init__(self, commands=()):
        super(WrappedMacroBuilder, self).__init__(commands)
        self.before_commands = []
        self.after_commands = []

    def add_before(self, builder, prepend=True):
        if prepend:
            self.before_commands.insert(0, builder)
        else:
            self.before_commands.append(builder)

    def add_after(self, builder):
        self.after_commands.append(builder)

    def wrap(self, wrapper, prepend=True):
        """

        :type wrapper: MacroWrapper
        """
        self.add_before(wrapper.before, prepend)
        self.add_after(wrapper.after)

    @property
    def commands(self):
        yield self.before_commands
        yield self._commands
        yield self.after_commands


class MacroBuilderWrapper(object):
    def before(self):
        return []

    def after(self):
        return []