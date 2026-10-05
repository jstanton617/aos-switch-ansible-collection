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

"""arubaoss_facts gathers its default subsets.

ansible.netcommon's FactsBase.get_network_legacy_facts() reads `.warnings`
from every legacy facts class. Removing that attribute, as #101 does, fails
every gather with "'HostSystemInfo' object has no attribute 'warnings'" -
which is what three switches answered on 2026-10-05.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest

from ansible_collections.arubanetworks.aos_switch.plugins.modules import arubaoss_facts
from ansible_collections.arubanetworks.aos_switch.tests.unit.plugins.modules.aoss_harness import (
    FakeSwitch, run_module)


def a_switch():
    return FakeSwitch({
        '/system/status/switch': {'switch_type': 'ST_STANDALONE'},
        '/modules': {'module_info': []},
        '/system/status/power/supply': {'system_power_supply': []},
    })


class TestFacts(unittest.TestCase):

    def test_the_default_subsets_are_gathered(self):
        result = run_module(arubaoss_facts, {}, a_switch())
        self.assertFalse(result.get('failed'), result)
        facts = result.get('ansible_facts', {})
        self.assertEqual(facts['ansible_net_host_system_info']['firmware_version'], 'WC.16.10.0012')
        self.assertEqual(facts['ansible_net_switch_specific_system_info'],
                         {'switch_type': 'ST_STANDALONE'})


if __name__ == '__main__':
    unittest.main()
