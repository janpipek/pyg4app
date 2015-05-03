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
                if isinstance(iterator, basestring):
                    iterator = (iterator,)

            elif isinstance(command, basestring):
                iterator = (command,)
            elif hasattr(command, "__iter__"):
                builder = MacroBuilder(command)
                iterator = builder.render()

            # 3. get all lines from the iterator
            for line in iterator:
                yield line

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
            for line in self.render():
                f.write(line + "\n")                


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