OpenStack Flavors
=================

This role can be used to register flavors in nova using the
openstack.cloud.compute\_flavor module.

Requirements
------------

The OpenStack nova API should be accessible from the target host.

Role Variables
--------------

`os_flavors_venv` is a path to a directory in which to create a
virtualenv.

`os_flavors_auth_type` is an authentication type compatible with
the `auth_type` argument of `os_*` Ansible modules.

`os_flavors_auth` is a dict containing authentication information
compatible with the `auth` argument of `os_*` Ansible modules.

`os_flavors_cacert` is an optional path to a CA certificate bundle.

`os_flavors_interface` is the endpoint URL type to fetch from the service
catalog. Maybe be one of `public`, `admin`, or `internal`.

`os_flavors` is a list of nova flavors to register. Each item should be a dict
containing the items 'name', 'ram', 'disk', and 'vcpus'. Optionally, the dict
may contain 'ephemeral', 'flavorid', 'rxtx_factor' and 'swap' items.
Optionally, the dict may also contain an item 'extra_specs', which is a dict of
metadata to attach to the flavor object.

Dependencies
------------

This role depends on the `stackhpc.os_openstacksdk` role.

Example Playbook
----------------

The following playbook registers a nova flavor.

    ---
    - name: Ensure nova flavors are registered
      hosts: nova-api
      roles:
        - role: os-flavors
          os_flavors_venv: "~/os-flavors-venv"
          os_flavors_auth_type: "password"
          os_flavors_auth:
            project_name: <keystone project>
            username: <keystone user>
            password: <keystone password>
            auth_url: <keystone auth URL>
          os_flavors:
            - name: flavor-1
              ram: 1024
              disk: 1024
              vcpus: 2
              extra_specs:
                hw:cpu_policy: "dedicated"
                hw:numa_nodes: "1"

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
