import functools

import config


def check_zy_chat(func):
    @functools.wraps(func)
    def decorator_check_zy_chat(*args, **kwargs):
        update = args[0]
        chatid = str(update.effective_chat.id)[4:]
        valid_chats = config.get_zychats()
        if chatid in valid_chats:
            func(*args, **kwargs)
        else:
            update.effective_message.reply_text("此群暂时不支持交作业、查询作业、删除作业等操作哦")
    return decorator_check_zy_chat


def check_admin_permission(uid):
    # 检查uid是否为管理员
    admin_uids = config.get_admin_uids()
    if uid not in admin_uids:
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
