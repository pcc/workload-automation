#    Copyright 2014-2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import textwrap

from wa.framework.plugin import Plugin
from wa.framework.version import get_wa_version
from wa.utils.doc import format_body


def init_argument_parser(parser):
    parser.add_argument('-c', '--config', action='append', default=[],
                        help='specify an additional config.py')
    parser.add_argument('-v', '--verbose', action='count',
                        help='The scripts will produce verbose output.')
    parser.add_argument('--version', action='version', 
                        version='%(prog)s {}'.format(get_wa_version()))
    return parser


class Command(Plugin):
    """
    Defines a Workload Automation command. This will be executed from the
    command line as ``wa <command> [args ...]``. This defines the name to be
    used when invoking wa, the code that will actually be executed on
    invocation and the argument parser to be used to parse the reset of the
    command line arguments.

    """
    kind = "command"
    help = None
    usage = None
    description = None
    epilog = None
    formatter_class = None

    def __init__(self, subparsers):
        super(Command, self).__init__()
        self.group = subparsers
        desc = format_body(textwrap.dedent(self.description), 80)
        parser_params = dict(help=(self.help or self.description), usage=self.usage,
                             description=desc, epilog=self.epilog)
        if self.formatter_class:
            parser_params['formatter_class'] = self.formatter_class
        self.parser = subparsers.add_parser(self.name, **parser_params)
        init_argument_parser(self.parser)  # propagate top-level options
        self.initialize(None)

    def initialize(self, context):
        """
        Perform command-specific initialisation (e.g. adding command-specific
        options to the command's parser). ``context`` is always ``None``.

        """
        pass

    def execute(self, state, args):
        """
        Execute this command.

        :state: An initialized ``ConfigManager`` that contains the current state of
                WA exeuction up to that point (processed configuraition, loaded
                plugins, etc).
        :args: An ``argparse.Namespace`` containing command line arguments (as 
               returned by ``argparse.ArgumentParser.parse_args()``. This would
               usually be the result of invoking ``self.parser``.

        """
        raise NotImplementedError()
