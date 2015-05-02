from .macro import Macro, MacroBuilder
from .configuration import Configuration
from .gui import Gui
from .runner import execute


class Application(MacroBuilder):
    '''A single execution of the application.'''
    def __init__(self, **kwargs):
        super(Application, self).__init__()
        self._plugins = []
        self.runs = []
        self.random = kwargs.get("random", True)
        self.log_events = kwargs.get("log_events", 1000)
        self.interactive = kwargs.get("interactive", False)
        self.configuration = kwargs.get("configuration", Configuration())
        self._kwargs = kwargs
        self.events = 0

    def add_plugin(self, path):
        self._plugins.append(path)

    def add_run(self, run):
        self.runs.append(run)

    def on_rendering(self):
        pass

    def pre_initialize(self):
        '''Override this.'''
        return []

    def post_initialize(self):
        '''Override this.'''
        return []

    @property
    def commands(self):
        # Prepare app for rendering
        self.on_rendering()

        yield None

        for plugin in self._plugins:
            if not plugin.endswith(".so"):
                # TODO: Works only on linux
                plugin = "lib" + plugin + ".so"
            yield "/app/plugin/load " + plugin

        if self.random:
            yield "/app/generateRandomSeed"

        yield self.pre_initialize()
        yield "/run/initialize"
        yield self.post_initialize()

        yield self.configuration

        if self.log_events:
            yield "/app/addAction NumberingEventAction"
            yield "/app/setInt app.logEvents %d" % self.log_events
        yield "/app/addAction MemoryRunAction"

        if self.interactive:
            if len(self._runs) > 1:
                raise BaseException("Only one run enabled in interactive mode.")
            elif self.runs:
                run = self.runs[0]
                yield run.before_commands
            yield "/app/prepareInteractive"
            yield Gui()
            yield "/app/interactive"
        else:
            yield self.runs

    def execute(self, events=None, interactive=None, **kwargs):
        '''Execute the application.'''
        if events is not None:
            self.events = events
        if interactive is not None:
            self.interactive = interactive
        macro = Macro()
        macro.add(self)
        execute(macro, **kwargs)

    def write(self, path):
        '''Just write the macro commands to a file.

        :param path: path of the output macro file

        Running g4 application with the macro file has same result as self.run().'''
        macro = Macro()
        macro.add(self)
        macro.write(path)