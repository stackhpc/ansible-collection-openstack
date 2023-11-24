OpenStack Container Clusters
============================

This role can be used to register container cluster templates in magnum
using the magnum CLI.

Requirements
------------

The OpenStack magnum API should be accessible from the target host.

Role Variables
--------------

`os_container_clusters_venv` is a path to a directory in which to create a
virtualenv.

`os_container_clusters_auth_type` is an authentication type compatible with the
`auth_type` argument of `os_*` Ansible modules.

`os_container_clusters_auth` is a dict containing authentication information
compatible with the `auth` argument of `os_*` Ansible modules.

`os_container_clusters_cacert` is an optional path to a CA certificate bundle.

`os_container_clusters_templates` is a list of magnum container cluster
templates to register. Each item should be a dict containing container cluster
template attributes.

Dependencies
------------

This role depends on the `stackhpc.os-shade` role.

Example Playbook
----------------

The following playbook registers a cluster template.

    ---
    - name: Ensure cluster templates are registered
      hosts: localhost
      roles:
        - role: os-container-clusters
          os_container_clusters_venv: "~/os-container-clusters-venv"
          os_container_clusters_auth_type: "password"
          os_container_clusters_auth:
            project_name: <keystone project>
            username: <keystone user>
            password: <keystone password>
            auth_url: <keystone auth URL>
          os_container_clusters_templates:
            - name: swarm-cluster
              coe: swarm
              master_flavor: m1.small
              flavor: m1.small
              image: fedora-25
              external_network: ext
              floating_ip_disabled: # leave empty to pass as flag without assigning value
              labels:
                etcd_volume_size: 3

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
