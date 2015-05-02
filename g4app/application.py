from .macro import MacroBuilder
from .configuration import Configuration
from .gui import Gui
from .runner import execute


class Application(MacroBuilder):
    '''A single execution of the application.'''
    def __init__(self, **kwargs):
        super(Application, self).__init__()
        self.components = []
        self._plugins = []
        self.runs = []

        self.random = kwargs.get("random", True)
        self.log_events = kwargs.get("log_events", 1000)
        self.interactive = kwargs.get("interactive", False)
        self.configuration = kwargs.get("configuration", Configuration())
        self._kwargs = kwargs
        self.events = 0

    def add_component(self, component):
        self.components.append(component)

    def add_plugin(self, name):
        self._plugins.append(name)

    def add_run(self, run):
        self.runs.append(run)

    def pre_initialize(self):
        return ()

    def post_initialize(self):
        return ()

    def pre_run(self, run):
        return ()

    @property
    def plugins(self):
        res = list(self._plugins)
        for component in self.components:
            res.extend(component.plugins)
        return res

    def on_rendering(self):
        pass

    @property
    def commands(self):
        self.on_rendering()

        # Prepare app for rendering
        yield None

        for plugin in self.plugins:
            if not plugin.endswith(".so"):
                # TODO: Works only on linux
                plugin = "lib" + plugin + ".so"
            yield "/app/plugin/load " + plugin

        if self.random:
            yield "/app/generateRandomSeed"

        # Run initialization
        yield self.pre_initialize()
        for component in self.components:
            yield component.pre_initialize()
        yield "/run/initialize"
        yield self.post_initialize()
        for component in self.components:
            yield component.post_initialize()

        # Configuration
        yield self.configuration

        if self.log_events:
            yield "/app/addAction NumberingEventAction"
            yield "/app/setInt app.logEvents %d" % self.log_events
        yield "/app/addAction MemoryRunAction"

        if self.interactive:
            runs = self.runs
            if len(runs) > 1:
                raise BaseException("Only one run enabled in interactive mode.")
            elif runs:
                run = runs[0]
                yield self.pre_run(run=run)
                for component in self.components:
                    yield component.pre_run(run=run)
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
        execute(self, **kwargs)

class Component(object):
    @property
    def plugins(self):
        return ()

    def pre_initialize(self):
        return None

    def post_initialize(self):
        return None

    def pre_run(self, run):
        return None

