OpenStack Host Aggregates
=========================

This role can be used to register host aggregates in nova using the
os\_nova\_host\_aggregate module.

Requirements
------------

The OpenStack nova API should be accessible from the target host.

Role Variables
--------------

`os_host_aggregates_venv` is a path to a directory in which to create a
virtualenv.

`os_host_aggregates_auth_type` is an authentication type compatible with the
`auth_type` argument of `os_*` Ansible modules.

`os_host_aggregates_auth` is a dict containing authentication information
compatible with the `auth` argument of `os_*` Ansible modules.

`os_host_aggregates_cacert` is an optional path to a CA certificate bundle.

`os_host_aggregates_interface` is the endpoint URL type to fetch from the
service catalog. Maybe be one of `public`, `admin`, or `internal`.

`os_host_aggregates` is a list of nova host aggregates to register. Each item
should be a dict containing the item 'name', and optionally:

* 'availability_zone' (name of the availability zone to set on the aggregate)
* 'hosts' (list of hostnames to add to the aggregate)
* 'metadata' (dict of key/value pairs to set on the aggregate)

Dependencies
------------

This role depends on the `stackhpc.os_openstacksdk` role.

Example Playbook
----------------

The following playbook registers a nova host aggregate.

    ---
    - name: Ensure nova host aggregates are registered
      hosts: nova-api
      roles:
        - role: stackhpc.os_host_aggregates
          os_host_aggregates_venv: "~/os-host-aggregates-venv"
          os_host_aggregates_auth_type: "password"
          os_host_aggregates_auth:
            project_name: <keystone project>
            username: <keystone user>
            password: <keystone password>
            auth_url: <keystone auth URL>
          os_host_aggregates:
            - name: db_aggregate
              availability_zone: az1
              hosts:
                - host1
                - host2
              metadata:
                type: dbcluster

Author Information
------------------

- Pierre Riteau (<pierre@stackhpc.com>)
