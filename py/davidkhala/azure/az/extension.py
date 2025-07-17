# TODO WIP
from azure.cli.core import AzCommandsLoader


class MyExtensionCommandsLoader(AzCommandsLoader):
    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        custom_type = CliCommandType(operations_tmpl='azext_myextension#{}')
        super(MyExtensionCommandsLoader, self).__init__(cli_ctx=cli_ctx, custom_command_type=custom_type)

    def load_command_table(self, args):
        with self.command_group('hello') as g:
            g.custom_command('world', 'say_hello')
        return self.command_table

    def load_arguments(self, _):
        pass

COMMAND_LOADER_CLS = MyExtensionCommandsLoader

def say_hello():
    print("Hello from your custom Azure CLI extension!")
