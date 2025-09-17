OpenStack Projects
==================

This role can be used to register projects, users and related resources in
OpenStack using the `openstack.cloud` modules.

Requirements
------------

The OpenStack Keystone API should be accessible from the target host.

Role Variables
--------------

`os_projects_venv` is a path to a directory in which to create a
virtualenv.

`os_projects_auth_type` is an authentication type compatible with
the `auth_type` argument of `openstack.cloud` Ansible modules.

`os_projects_auth` is a dict containing authentication information
compatible with the `auth` argument of `openstack.cloud` Ansible modules.

`os_projects_region` is an optional name of an OpenStack region.

`os_projects_cacert` is an optional path to a CA certificate bundle.

`os_projects_cloud` is an optional name of a cloud in `clouds.yaml`.

`os_projects_interface` is the endpoint URL type to fetch from the service
catalog. Maybe be one of `public`, `admin`, or `internal`.

`os_projects_domains` is a list of OpenStack domains to create.
Each item should be a dict containing the following items:
- `name`: The name of the domain.
- `description`: Optional description for the domain.

`os_projects` is a list of projects to register.
Each item should be a dict containing the following items:
- `name`: The name of the project.
- `description`: A description of the project.
- `project_domain`: The domain in which to register the project.
- `user_domain`: The domain in which to register users.
- `users`: Optional list of users to register. Each user should be a dict
  containing the following items:
  - `name`: The name of the user.
  - `description`: User name/description (optional)
  - `email`: User email address (optional)
  - `password`: The user's password (optional). This is not updated after
    creation.
  - `roles`: Optional list of roles to assign to the user in the project.
  - `domain_roles`: Optional list of roles to assign to the user in the user
    domain.
  - `openrc_file`: Path to an environment file to create.
  - `create_user`: Boolean to indicate whether or not to create the user.  Can
    be useful if the user already exists e.g the user is defined in LDAP.
    (optional)
- `keypairs`: Optional list of SSH key pairs to register with Nova. Each key
  pair should be a dict containing the following items:
  - `name`: The name of the keypair.
  - `public_key`: The SSH public key contents. Optional.
  - `public_key_file`: Path to the SSH public key on the control host.
- `quotas`: Optional dict mapping quota names to their values.

`os_projects_upper_constraints_file` is a path to an upper constraints file which
is passed through to the role dependencies.

Dependencies
------------

This role depends on the `stackhpc.openstack.os_openstacksdk` and
`stackhpc.openstack.os_openstackclient` roles.

Example Playbook
----------------

The following playbook registers an OpenStack project, users and related
resources.

    ---
    - name: Ensure OpenStack projects are registered
      hosts: localhost
      roles:
        - role: stackhpc.openstack.os_projects
          os_projects_venv: "~/os-projects-venv"
          os_projects_upper_constraints_file: "https://releases.openstack.org/constraints/upper/2024.1"
          os_projects_auth_type: "password"
          os_projects_auth:
            project_name: <keystone project>
            username: <keystone user>
            password: <keystone password>
            auth_url: <keystone auth URL>
          os_projects:
            - name: project1
              description: An example project
              project_domain: default
              user_domain: default
              users:
                - name: user1
                  password: correcthorsebatterystaple
                  roles:
                    - admin
                  openrc_file: /home/user/user1.openrc
              keypairs:
                - name: keypair1
                  public_key_file: /path/to/key
              quotas:
                ram: -1

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
