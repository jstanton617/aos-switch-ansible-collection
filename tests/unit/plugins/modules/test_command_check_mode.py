# Copyright (c) 2026 James Stanton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""arubaoss_command sends only `show` commands in check mode.

It declares supports_check_mode=True and had no check-mode handling, so a
--check run sent every command it was given: `erase config`, `configure
terminal` and all. ansible.netcommon's cli_command and vyos.vyos' vyos_command
both run only `show` commands in check mode, and say what they skipped.

The connection is replaced at the module's boundary, and records what the
module hands it.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest

from unittest import mock

from ansible_collections.arubanetworks.aos_switch.plugins.module_utils import arubaoss
from ansible_collections.arubanetworks.aos_switch.plugins.modules import arubaoss_command
from ansible_collections.arubanetworks.aos_switch.tests.unit.plugins.modules.aoss_harness import (
    FakeSwitch, run_module)

COMMANDS = ['show config files', 'configure terminal',
            'startup-default primary config rollback', 'end', 'erase config rollback']


def run_recording(check_mode):
    """(result, the commands the module sent to its connection)."""
    sent = []

    class Recording(object):
        def __init__(self, socket_path):
            pass

        def run_commands(self, commands=None, check_rc=False):
            sent.extend(c['command'] for c in commands)
            return [''] * len(commands)

    with mock.patch.object(arubaoss, 'Connection', Recording):
        result = run_module(arubaoss_command, {'commands': COMMANDS}, FakeSwitch(),
                            check_mode=check_mode)
    return result, sent


class TestCommandCheckMode(unittest.TestCase):

    def test_check_mode_sends_only_the_show_commands(self):
        result, sent = run_recording(check_mode=True)
        self.assertFalse(result.get('failed'), result)
        self.assertEqual(sent, ['show config files'])
        warnings = [w['event']['msg'] if isinstance(w, dict) else w
                    for w in result.get('warnings', [])]
        self.assertTrue(any('erase config rollback' in w for w in warnings), warnings)

    def test_a_normal_run_sends_every_command(self):
        result, sent = run_recording(check_mode=False)
        self.assertEqual(sent, COMMANDS)


if __name__ == '__main__':
    unittest.main()
