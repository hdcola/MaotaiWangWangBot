

import config


def check_admin_permission(chatid):
    admin_chatids = config.get_admin_chatids()
    if chatid not in admin_chatids:
        return False
    else:
        return True
    

def check_chatids_valid(chatids):
    for i in chatids:
        if not _check_chatid_valid(i):
            return False
    return True

def _check_chatid_valid(chatid):
    if len(chatid) > 1 and (chatid[0] == '-' or chatid[0].isnumeric()) and chatid[1:].isnumeric():
        return True
    else:
        return False


