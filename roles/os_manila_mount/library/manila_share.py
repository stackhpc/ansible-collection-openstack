#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule


import openstack


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True, type='str'), # share name 
            access_to=dict(required=True, type='str'), # rule "access to" parameter
        ),
        supports_check_mode=False
    )

    result = dict(changed=False)
    share_name = module.params['name']
    access_to = module.params['access_to']
    conn = openstack.connection.from_config()
    share = conn.share.find_share(share_name)
    if share is None:
        module.fail_json('No share named %r found' % share_name)
    access_rules = list(conn.share.access_rules(share))
    rules = [v for v in access_rules if v.access_to == access_to]
    if len(rules) == 0:
        module.fail_json("No rules found with 'access_to=%r' for share named %r" % (access_to, share_name))
    if len(rules) != 1:
        module.fail_json("Multiple rules found with 'access_to=%r' for share named %r" % (access_to, share_name))
    rule = rules[0]
    # the share object doesn't actually expose lots of stuff from the API, including the exports
    share_details = conn.share.get(f"/shares/{share.id}").json()['share']
    result['share'] = share_details
    result['rule'] = rule
    module.exit_json(**result)

if __name__ == '__main__':
    main()
