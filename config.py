#!/usr/bin/env python3

import json
import os

loads = json.loads
load = json.load
dumps = json.dumps
dump = json.dump

config_file = ""
config_path = "~/.config/maotaibot/"
run_path = os.path.split(os.path.realpath(__file__))[0]

MAX_ZY_NUM = 7



"""
zy 格式设计
为了应对未来可能有的查某个人的所有作业情况，加入 uid作为key，方便快速检索
{
    uid1：
    {
        "UID": uid1,
        "FirstName": firstname,
        "ZY": [
            {
                "DATETIME": datetime1,
                "MESSAGEID": messageid1
            },
            {
                "DATETIME": datetime2,
                "MESSAGEID": messageid2
            }
        ]
    }
    uid2:
    {
        "UID": uid2,
        "FirstName": firstname,
        "ZY": [
            {
                "DATETIME": datetime1,
                "MESSAGEID": messageid1
            },
            {
                "DATETIME": datetime2,
                "MESSAGEID": messageid2
            }
        ]
    }
}
"""



def load_all_zy():
    """
    load zy.config, 获取所有人的作业
    """
    zy_filepath = os.path.join(os.path.expanduser(config_path), f"zy.json")
    if not os.path.exists(zy_filepath):
        return {}
    else:
        with open(zy_filepath, 'r') as zyfile:
            return load( zyfile )


def _save_all_zy(zys):
    """
    存储所有人的作业到 zy.config
    """
    zy_path = os.path.dirname(os.path.expanduser(config_path))
    if not os.path.exists(zy_path):
        os.makedirs(zy_path, exist_ok=True)
    
    zy_filepath = os.path.join(zy_path, f"zy.json")
    with open(zy_filepath, 'w') as zyfile:
        dump(zys, zyfile, indent=4, ensure_ascii=False)




def load_zy(uid):
    # load 某人的作业
    all_zys = load_all_zy()
    return all_zys.get(str(uid), {})


def save_zy(uid, zys):
    # 存某人的作业
    all_zys = load_all_zy()
    all_zys[str(uid)] = zys
    _save_all_zy(all_zys)



CONFIG = {}

def load_config():
    global CONFIG
    with open(config_file, 'r') as configfile:
        CONFIG = load( configfile )
    return CONFIG

def save_config():
    file_dir = os.path.split(config_file)[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    with open(config_file, 'w') as configfile:
        dump(CONFIG, configfile, indent=4,ensure_ascii=False)

def get_json():
    return dumps(CONFIG,indent=4,ensure_ascii=False)

def set_default():
    # (filepath,filename) = os.path.split(config_file)
    # folder = os.path.exists(filepath)
    # if not folder:
    #     os.makedirs(filepath)
    load_config
    CONFIG.setdefault("Token","")       #BotToken
    CONFIG.setdefault("Admin",[])       #管理员id
    CONFIG.setdefault("Admin_path","")  #Admin Shell Path
    save_config()

def get_admin_chatids():
    if not CONFIG:
        load_config()
    return CONFIG.get("Admin", [])


def set_cmd(cmds):
    CONFIG["CMDS"] = cmds
    save_config()

def get_cmd():
    cmds = CONFIG.setdefault("CMDS", [])
    return cmds
    