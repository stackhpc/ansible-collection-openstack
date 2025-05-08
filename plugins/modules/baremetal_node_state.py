#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2015, Hewlett-Packard Development Company, L.P.
# Copyright 2017 StackHPC Ltd.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: baremetal_node_state
short_description: Set provision state of Bare Metal Resources from OpenStack
author: "Mark Goddard <mark@stackhpc.com>"
extends_documentation_fragment: openstack
description:
    - Set the provision state of OpenStack ironic bare metal nodes.
options:
    provision_state:
      description:
        - Indicates desired provision state of the resource
      choices: ['manage', 'provide']
      default: present
    uuid:
      description:
        - globally unique identifier (UUID) to be given to the resource.
      required: false
      default: None
    ironic_url:
      description:
        - If noauth mode is utilized, this is required to be set to the
          endpoint URL for the Ironic API.  Use with "auth" and "auth_type"
          settings set to None.
      required: false
      default: None
    wait:
      description:
        - A boolean value instructing the module to wait for node
          activation or deactivation to complete before returning.
      required: false
      default: False
      version_added: "2.1"
    timeout:
      description:
        - An integer value representing the number of seconds to
          wait for the node activation or deactivation to complete.
      version_added: "2.1"
    availability_zone:
      description:
        - Ignored. Present for backwards compatibility
      required: false
'''

EXAMPLES = r'''
baremeta_node_state:
  cloud: "openstack"
  uuid: "d44666e1-35b3-4f6b-acb0-88ab7052da69"
  provision_state: provide
  delegate_to: localhost
'''

from ansible_collections.openstack.cloud.plugins.module_utils.openstack import (
    OpenStackModule
)


def _choose_id_value(module):
    if module.params['uuid']:
        return module.params['uuid']
    if module.params['name']:
        return module.params['name']
    return None


def _change_required(current_provision_state, action):
    """Return whether a change to the provision state is required.

    :param current_provision_state: The current provision state of the node.
    :param action: The requested action.
    """
    if action == 'manage':
        if current_provision_state == 'manageable':
            return False
    if action == 'provide':
        if current_provision_state == 'available':
            return False
    return True


class BaremetalDeployTemplateModule(OpenStackModule):
    argument_spec = dict(
        uuid=dict(required=False),
        name=dict(required=False),
        ironic_url=dict(required=False),
        provision_state=dict(required=True,
                             choices=['manage', 'provide']),
        wait=dict(type='bool', required=False, default=False),
        timeout=dict(required=False, type='int', default=1800),
    )
    module_kwargs = dict(
        required_one_of=[
            ('uuid', 'name'),
        ],
    )

    def run(self):
        if (self.params['auth_type'] in [None, 'None'] and
                self.params['ironic_url'] is None):
            self.fail_json(msg="Authentication appears disabled, Please "
                                 "define an ironic_url parameter")

        if (self.params['ironic_url'] and
                self.params['auth_type'] in [None, 'None']):
            self.params['auth'] = dict(
                endpoint=self.params['ironic_url']
            )

        node_id = _choose_id_value(self)

        if not node_id:
            self.fail_json(msg="A uuid or name value must be defined "
                                 "to use this module.")

        try:
            sdk, cloud = openstack_cloud_from_module(self)
            node = cloud.get_machine(node_id)

            if node is None:
                self.fail_json(msg="node not found")

            uuid = node['uuid']
            changed = False
            wait = self.params['wait']
            timeout = self.params['timeout']
            provision_state = self.params['provision_state']

            if node['provision_state'] in [
                    'cleaning',
                    'deleting',
                    'wait call-back']:
                self.fail_json(msg="Node is in %s state, cannot act upon the "
                                     "request as the node is in a transition "
                                     "state" % node['provision_state'])

            if _change_required(node['provision_state'], provision_state):
                cloud.node_set_provision_state(uuid, provision_state, wait=wait,
                                               timeout=timeout)
                changed = True

            self.exit_json(changed=changed)

        except Exception as e:
            self.fail_json(msg=str(e))


def main():
    module = BaremetalNodeStateModule()
    module()


if __name__ == "__main__":
    main()
