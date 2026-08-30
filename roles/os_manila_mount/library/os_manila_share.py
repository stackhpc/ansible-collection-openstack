#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

import openstack

ANSIBLE_METADATA = {'metadata_version': '1.0'}


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            # passthrough=dict(optional=False, type='dict'),
        ),
        supports_check_mode=False
    )

    result = dict(changed=False)
    share_name = module.params['name']
    user = module.params['user']
    conn = openstack.connection.from_config()
    share = conn.share.find_share(share_name)
    if share is None:
        module.fail_json('No share named %r found' % share_name)
    
    # the share object doesn't actually expose lots of stuff from the API, including the exports
    share_details = conn.share.get(f"/shares/{share.id}").json()['share']
    # module.fail_json(share_details) # DEBUG
    protocol = share_details['share_proto'].upper()
    if protocol != 'CEPHFS':
        module.fail_json("Share named %r is protocol %r, can only handle CEPHFS" % (share_name, protocol))
    
    # find host and path from CephFS export of form 'mon1:port,mon2:port,mon3:port:path'
    host, export_path = share_details['export_location'].rsplit(':', 1)

    # find rule:
    access_rules = list(conn.share.access_rules(share))
    rules = [v for v in access_rules if v.access_to == user]
    if len(rules) == 0:
        module.fail_json("No rules found with 'access_to=%s' for share named %r" % (access_to, share_name))
    if len(rules) != 1:
        module.fail_json("Multiple rules found with 'access_to=%s' for share named %r" % (access_to, share_name))
    rule = rules[0]

    # Put required parameters at top level in result to make loops easy:
    result['host'] = host
    result['export'] = export_path
    result['access_key'] = rule['access_key']
    
    # # Add passthrough parameters to make loops easy:
    # for k, v in passthrough.items():
    #     if k in result:
    #         module.fail_json("Passthrough parameter %r overwrites discovered parameter from share named %r" % (k, share_name))
    #     result[k] = v

    # result['rule'] = rule
    # TODO: add more info here?
    module.exit_json(**result)

if __name__ == '__main__':
    main()
