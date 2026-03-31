from prismacloud.api import pc_api

from apu.access_keys import core

# pc_api https://github.com/PaloAltoNetworks/prismacloud-api-python/
# prismacloud/api/cspm/_endpoints.py


def rotate_key(key, allow_delete=False, delete_if_expired=False):
    # {
    #     'id': '<uuid access key>',
    #     'name': 'zwaqar-ssut',
    #     'createdBy': '<email>',
    #     'createdTs': 1770151324838,
    #     'lastUsedTime': 1770151324838,
    #     'status': 'expired',
    #     'expiresOn': 1770237720121,
    #     'role': {d
    #         'id': '<role uuid>',
    #         'name': 'System Admin'
    #     },
    #     'roleType': 'System Admin',
    #     'username': 'zwaqar@paloaltonetworks.com'
    # }
    key_list = pc_api.access_keys_list_read()

    key_found = None
    access_keys_owned_by_user = 0  # len([obj for obj in key_list if obj.get('username') == key_found.get('username')])
    for key_entry in key_list:
        if key.get("id") == key_entry.get("id"):
            key_found = key_entry
            if core.is_expired(key_found) and delete_if_expired:
                core.delete(key)  # reference logic unused for now.
                continue  # Do not add to the count of existing access keys if you just deleted it.

    if not key_found:
        raise Exception("Key not found")

    for key_entry in key_list:
        if key_entry.get("username") == key_found.get("username"):
            access_keys_owned_by_user += 1

    if access_keys_owned_by_user == 2:
        if allow_delete:
            pc_api.access_key_delete(key_found)
        else:
            raise Exception(
                "1 of 2 keys owned by this user must be delete to create a new one."
            )
    return core.add(key_found)


"""
Users and service accounts can have 0, 1, or 2 access keys.
If there are already 2 then one must be deleted before creating another.
The assumption in this scrcipt is that if you 'allow_delete' the key you are trying to rotate has expired and should be deleted.
Else it will raise an error suggesting direction on what key to delete.
I could add logic to check the expiration of the key but, this does not imply the intentions of the user
"""
