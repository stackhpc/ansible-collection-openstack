OpenStack Cloudkitty Ratings
============================

This role can be used to register ratings in OpenStack Cloudkitty.

Requirements
------------

The OpenStack Cloudkitty API should be accessible from the target host.

Role Variables
--------------

`os_ratings_venv` is a path to a directory in which to create a
virtual environment.

`os_ratings_upper_constraints_file` is a file or URL containing Python
upper constraints.

`os_ratings_environment` is a dict of environment variables for use with
OpenStack CLI. Default is empty.

`os_ratings_hashmap_field_mappings` is a list of mappings associated with a
field.  Each item is a dict with the following fields:
* `service`
* `name`
* `mappings`
The mappings field is a list, where each item is a dict with the following
fields:
* `value`
* `cost`
* `group` (optional)
* `type`

`os_ratings_hashmap_service_mappings` is a list of mappings not associated with
a field.  Each item is a dict with the following fields:
* `service`
* `cost`
* `group` (optional)
* `type`

Dependencies
------------

This role depends on the `stackhpc.openstack.os_openstackclient` role.

Example Playbook
----------------

The following playbook registers a Cloudkitty flavor field with two mappings
for different Nova flavors. It also registers a service mapping based on the
size of images stored in Glance.

```
---
- name: Ensure Cloudkitty ratings are registered
  hosts: os-client
  tasks:
    - import_role:
        name: stackhpc.openstack.os_ratings
      vars:
        os_ratings_venv: "~/os-ratings-venv"
        os_ratings_environment:
          OS_AUTH_URL: "{{ lookup('env', 'OS_AUTH_URL') }}"
          ...
        os_ratings_hashmap_field_mappings:
          - service: instance
            name: flavor_id
            mappings:
              - value: small
                cost: 1.0
                group: instance_uptime_flavor_id
                type: flat
              - value: large
                cost: 2.0
                group: instance_uptime_flavor_id
                type: flat
        os_ratings_hashmap_service_mappings:
          - service: image.size
            cost: 0.1
            group: volume_ceph
            type: flat
```

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
