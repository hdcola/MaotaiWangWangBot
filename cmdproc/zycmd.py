import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand, Message
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackQueryHandler, CallbackContext

import config
from json import loads
from utils import check_admin_permission

from datetime import datetime




def add_zy(zys, zy):
    """
    add zy to zys 
    需要处理时间的问题，一天只能保存一个数据
    同一天交多次作业，会默认保存最后一次作业内容
    """

    for _zy in zys:
        if _zy.get('DATETIME') == zy.get('DATETIME'):
            _zy['MESSAGEID'] = zy.get('MESSAGEID')
            return zys
    
    if len(zys) == config.MAX_ZY_NUM:
        zys = zys[1:]
    zys.append( zy )

    return zys



def zy_cmd(update: Updater, context: CallbackContext):
    uid = update.effective_user.id
    message = update.effective_message

    if not message.reply_to_message :
        update.effective_message.reply_text("同学，你需要使用 /zy 回复你的作业(作业应该是一个图片或文件)，用于提交作业哦")
        return
    
    if (not message.reply_to_message.photo) or (not message.reply_to_message.document):
        update.effective_message.reply_text("同学，你需要使用 /zy 回复你的作业(作业应该是一个图片或文件)，用于提交作业哦")
        return

    _messageid = update.effective_message.reply_to_message.message_id
    chatid = str(update.effective_chat.id)
    firstname = update.effective_user.first_name
    messageid = f"https://t.me/c/{chatid[4:]}/{_messageid}"

    zys = config.load_zy(uid)

    if not zys:
        # 首次交作业，初始化
        zys = {
            "UID": uid,
            "FirstName": firstname,
            "ZY": [
                {
                    "DATETIME": datetime.today().strftime("%m%d"),
                    "MESSAGEID": messageid
                },
            ]
        }
        config.save_zy(uid, zys)

    else: 
        _zys = zys.setdefault("ZY", [])

        _zy = {
            "DATETIME": datetime.now().strftime("%m%d"),
            "MESSAGEID": messageid
        }

        # 添加作业
        _zys = add_zy(_zys, _zy)

        zys["ZY"] = _zys

        config.save_zy(uid, zys)

    update.effective_message.reply_text("恭喜你提交作业成功~")


def lzy_cmd(update: Updater, context: CallbackContext):
    """
    获取所有人当前，或者某个具体日子的作业。
    日期格式MMDD
    """
    _datetime = datetime.now().strftime("%m%d")
    _command = update.effective_message.text.split("/lzy ")
    if len(_command) > 1:
        _datetime = _command[1].strip()
    if len(_datetime) != 4:
        update.effective_message.reply_text("命令格式输入错误，请使用 /lzy MMDD 的形式查询哦")
        return
    
    all_zys = config.load_all_zy()
    result = []
    print(all_zys)
    for uid, zy in all_zys.items():
        for _zy in zy.get('ZY', []):
            if _zy['DATETIME'] == _datetime:
                result.append([zy['FirstName'], _zy['MESSAGEID']])

    
    res =  os.linesep.join(map(lambda x: f"{x[0]}, {x[1]}", result))
    if not res:
        res = f"{_datetime}这一天没有人交作业哦"
        
    update.effective_message.reply_text(res)

def kzy_cmd(update: Updater, context: CallbackContext):
    pass

def add_dispatcher(dp: Dispatcher):
    # /zy 交作业
    dp.add_handler(CommandHandler("zy",zy_cmd))
    # /lzy 列出当天交的作业
    dp.add_handler(CommandHandler("lzy", lzy_cmd))
    # /kzy 列出所有的人交作业的情况，通过按钮来决定踢出一个没交作业的人
    dp.add_handler(CommandHandler("kzy", kzy_cmd))

    # dp.add_handler(CallbackQueryHandler(admin_command_callback,pattern="^zy:[A-Za-z0-9_]*"))
    return [BotCommand('zy','使用/zy回复你的作业后交作业'), BotCommand('lzy', '查看当天交的作业列表')]

