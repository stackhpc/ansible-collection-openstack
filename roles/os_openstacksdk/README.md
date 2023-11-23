OpenStack openstacksdk
======================

This role can be used to install the python package `openstacksdk`.

Requirements
------------

Linux - none, macOS - brew.sh

Role Variables
--------------

`os_openstacksdk_venv` is a path to a directory in which to create a
virtualenv.

`os_openstacksdk_install_epel`: Whether to install EPEL repository package.

`os_openstacksdk_install_package_dependencies`: Whether to install package
dependencies.

`os_openstacksdk_version`: Version of `openstacksdk` to install, or latest if
empty.

Dependencies
------------

None

Example Playbook
----------------

The following playbook installs openstacksdk and its dependencies in a virtualenv.

    ---
    - name: Ensure openstacksdk is installed
      hosts: localhost
      roles:
        - role: stackhpc.os_openstacksdk
          os_openstacksdk_venv: "~/os-openstacksdk-venv"

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
