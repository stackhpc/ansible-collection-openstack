OpenStack Flavors
=================

This role can be used to register flavors in Nova and map them to projects
using the `openstack.cloud.compute_flavor` module.

Requirements
------------

The OpenStack Nova API should be accessible from the target host.

Role Variables
--------------

`os_flavors_venv` is a path to a directory in which to create a
virtualenv.

`os_flavors_auth_type` is an authentication type compatible with
the `auth_type` argument of `openstack.cloud` Ansible modules.

`os_flavors_auth` is a dict containing authentication information
compatible with the `auth` argument of `openstack.cloud` Ansible modules.

`os_flavors_region_name` is an optional name of an OpenStack region.

`os_flavors_cacert` is an optional path to a CA certificate bundle.

`os_flavors_interface` is the endpoint URL type to fetch from the service
catalog. Maybe be one of `public`, `admin`, or `internal`.

`os_flavors` is a list of Nova flavors to register. Each item should be a dict
containing the items 'name', 'ram', 'disk', and 'vcpus'. Optionally, the dict
may contain 'ephemeral', 'flavorid', 'rxtx_factor' and 'swap' items.
Optionally, the dict may also contain an item 'extra_specs', which is a dict of
metadata to attach to the flavor object.

`is_public` default is `true`. It is a mandatory parameter when mapping
flavor to project, and it have to be set to `false` in that case. Public 
flavor can't be mapped. However there is possibility to create flavor which 
is private and not mapped to any project. Only 'true' and 'false' are 
allowed here.

`project` single value, or list of projects, to which flavor should be mapped. 
In other words: this flavor will be visible and usable only in said project(s).


Dependencies
------------

This role depends on the `stackhpc.openstack.os_openstacksdk` role.

Example Playbook
----------------

The following playbook registers a Nova flavor.

    ---
    - name: Ensure Nova flavors are registered
      hosts: localhost
      roles:
        - role: stackhpc.openstack.os_flavors
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

The following playbook will allow uasge of `flavor-1` only in project `projectA`.

    ---
    - name: Map Nova flavors to projects
      hosts: localhost
      roles:
        - role: openstack.cloud.compute_flavor_access
          os_flavors_venv: "~/os-flavors-venv"
          os_flavors_auth_type: "password"
          os_flavors_auth:
            project_name: <keystone project>
            username: <keystone user>
            password: <keystone password>
            auth_url: <keystone auth URL>
          os_flavors:
            - name: flavor-1
              is_public: false
              project: "projectA"

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
