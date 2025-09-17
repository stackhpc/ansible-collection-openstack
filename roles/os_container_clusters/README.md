OpenStack Container Clusters
============================

This role can be used to register container cluster templates in Magnum
using the Magnum CLI.

Requirements
------------

The OpenStack Magnum API should be accessible from the target host.

Role Variables
--------------

`os_container_clusters_venv` is a path to a directory in which to create a
virtualenv.

`os_container_clusters_auth_type` is an authentication type compatible with the
`auth_type` argument of `openstack.cloud` Ansible modules.

`os_container_clusters_auth` is a dict containing authentication information
compatible with the `auth` argument of `openstack.cloud` Ansible modules.

`os_container_clusters_region` is an optional name of an OpenStack region.

`os_container_clusters_cacert` is an optional path to a CA certificate bundle.

`os_container_clusters_templates` is a list of Magnum container cluster
templates to register. Each item should be a dict containing container cluster
template attributes.

`os_container_clusters_public`: whether to register templates as public by
default. Default is `false`.

`os_container_clusters_templates_hide` (optional) whether to hide the given
list of cluster templates by default. The `is_hidden` attribute can be used on
individual templates to specify this as well. Default is False.

Dependencies
------------

This role depends on the `stackhpc.openstack.os_openstackclient` and
`stackhpc.openstack.os_openstacksdk` roles.

Example Playbook
----------------

The following playbook registers a cluster template.

    ---
    - name: Ensure cluster templates are registered
      hosts: localhost
      roles:
        - role: stackhpc.openstack.os_container_clusters
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
