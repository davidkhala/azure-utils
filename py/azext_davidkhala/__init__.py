# TODO ugly azure extension
from azure.cli.core import AzCommandsLoader


def say_hello():
    print("Hello from your custom Azure CLI extension!")

class COMMAND_LOADER_CLS(AzCommandsLoader):
    def __init__(self, cli_ctx):
        from azure.cli.core.commands import CliCommandType
        super().__init__(cli_ctx=cli_ctx,custom_command_type=CliCommandType(operations_tmpl=__package__+"#{}"))

    def load_command_table(self, args):
        with self.command_group('hello') as g:
            g.custom_command('world', 'say_hello')
        return self.command_table


