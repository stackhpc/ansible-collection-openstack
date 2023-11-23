OpenStack Ironic deploy templates
=================================

This role can be used to register deploy templates in OpenStack ironic.

What are deploy templates? Read the
[docs](https://docs.openstack.org/ironic/latest/admin/node-deployment.html) or
watch the [video](https://www.youtube.com/watch?v=DrQcTljx_eM) to find out!

Requirements
------------

The OpenStack Ironic API should be accessible from the target host.

Role Variables
--------------

`os_deploy_templates_venv` is a path to a directory in which to create a
virtualenv.

`os_deploy_templates_upper_constraints_file` is a file or URL containing Python
upper constraints.

`os_deploy_templates_auth_type` is an authentication type compatible with
the `auth_type` argument of `os_*` Ansible modules.

`os_deploy_templates_auth` is a dict containing authentication information
compatible with the `auth` argument of `os_*` Ansible modules.

`os_deploy_templates_cacert` is an optional path to a CA certificate bundle.

`os_deploy_templates_interface` is the endpoint URL type to fetch from the service
catalog. Maybe be one of `public`, `admin`, or `internal`.

`os_deploy_templates` is a list of Ironic deploy templates to register. Each
item should be a dict containing following items:
* `name`: Name of the deploy template.
* `steps`: List of deploy steps.
* `extra`: Dict of metadata, optional.
* `uuid`: UUID, optional.
* `state`: State, optional.

Dependencies
------------

This role depends on the `stackhpc.os_openstacksdk` role.

Example Playbook
----------------

The following playbook registers an Ironic deploy template.

```
---
- name: Ensure Ironic deploy templates are registered
  hosts: os-clients
  tasks:
    - import_role:
        name: stackhpc.os_deploy_templates
      vars:
        os_deploy_templates_venv: "~/os-deploy_templates-venv"
        os_deploy_templates_auth_type: "password"
        os_deploy_templates_auth:
          project_name: <keystone project>
          username: <keystone user>
          password: <keystone password>
          auth_url: <keystone auth URL>
        os_deploy_templates:
          - name: CUSTOM_HYPERTHREADING_ENABLED
            steps:
              - interface: bios
                step: apply_configuration
                args:
                  settings:
                    - name: LogicalProc
                      value: Enabled
                priority: 110
```

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
