# The `homelab` branch

This branch is what [jstanton617/homelab](https://github.com/jstanton617/homelab)
installs, pinned by commit. It is upstream `master` (v1.7.0) plus open pull
requests that upstream has not reviewed:

| PR | Fixes |
|---|---|
| [#101](https://github.com/aruba/aos-switch-ansible-collection/pull/101) | `warnings` passed to `exit_json`, which ansible-core 2.23 removes (#100). By Kevin T. Berstene |
| [#109](https://github.com/aruba/aos-switch-ansible-collection/pull/109) | 34 modules claimed check-mode support they don't have (#105) |
| [#110](https://github.com/aruba/aos-switch-ansible-collection/pull/110) | A failed logout after a write hid the write's result (#104) |
| [#111](https://github.com/aruba/aos-switch-ansible-collection/pull/111) | `ansible.module_utils._text`, which ansible-core 2.24 removes (#108) |
| [#112](https://github.com/aruba/aos-switch-ansible-collection/pull/112) | CLI commands reported `ok` on a dead connection (#31) |
| [#113](https://github.com/aruba/aos-switch-ansible-collection/pull/113) | `device_operation_mode` was sent on every call (#106) |
| [#114](https://github.com/aruba/aos-switch-ansible-collection/pull/114) | `loop_protect` reset settings and misspelled two field names (#107) |

Each is merged as it stands on its PR. The one change of this branch's own is
`galaxy.yml`: `repository` names this fork, and the version is
`1.7.0+homelab.1`, so an install says where it came from.

The unit tests are in `tests/unit`, and run with:

```
python -m unittest ansible_collections.arubanetworks.aos_switch.tests.unit.plugins.<module>
```

from the directory that contains `ansible_collections/`, with
`ansible.netcommon` importable.
