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

ZY_PATH = "~/.config/zy/"
MAX_ZY_NUM = 7



"""
zy 格式设计
{
    "UID": uid,
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
"""
def load_zy(uid):

    zys = {}

    # load 某人的作业
    zy_filepath = os.path.join(os.path.expanduser(ZY_PATH), f"{uid}.json")
    if not os.path.exists(zy_filepath):
        return zys
    
    with open(zy_filepath, 'r') as zyfile:
        zys = load( zyfile )
    return zys



def save_zy(uid, zys):

    zy_path = os.path.dirname(os.path.expanduser(ZY_PATH))
    if not os.path.exists(zy_path):
        os.makedirs(zy_path, exist_ok=True)

    # save 某人的作业
    zy_filepath = os.path.join(zy_path, f"{uid}.json")
    with open(zy_filepath, 'w') as zyfile:
        dump(zys, zyfile, indent=4, ensure_ascii=False)




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
    