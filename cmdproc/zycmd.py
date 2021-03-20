import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand, Message, TelegramError
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackQueryHandler, CallbackContext

import config, utils
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
    zys.append(zy)

    return zys


def zy_cmd(update: Updater, context: CallbackContext):

    uid = update.effective_user.id
    message = update.effective_message

    if message.reply_to_message == None:
        update.effective_message.reply_text("同学，你需要使用 /zy 回复你的作业，用于提交作业哦")
        return
    elif message.reply_to_message.from_user.id != message.from_user.id:
        update.effective_message.reply_text("对不起同学，你只能提交自己的作业哦！")
        return

    if message.reply_to_message.photo == [] and message.reply_to_message.document == None:
        update.effective_message.reply_text("同学，你需要使用 /zy 回复你的作业(作业应该是一个图片或文件)，用于提交作业哦")
        return

    _messageid = update.effective_message.reply_to_message.message_id
    chatid = str(update.effective_chat.id)[4:]

    firstname = update.effective_user.first_name
    messageid = f"https://t.me/c/{chatid}/{_messageid}"

    zys = config.load_zy(chatid, uid)

    if not zys:
        # 首次交作业，初始化
        zys = {
            "UID": uid,
            "FirstName": firstname,
            "ZY": [{
                "DATETIME": datetime.today().strftime("%m%d"),
                "MESSAGEID": messageid
            }, ]
        }
        config.save_zy(chatid, uid, zys)

    else:
        _zys = zys.setdefault("ZY", [])

        _zy = {"DATETIME": datetime.now().strftime("%m%d"), "MESSAGEID": messageid}

        # 添加作业
        _zys = add_zy(_zys, _zy)

        zys["ZY"] = _zys

        config.save_zy(chatid, uid, zys)

    update.effective_message.reply_text("恭喜你提交作业成功~")


def lzy_cmd(update: Updater, context: CallbackContext):
    """
    获取所有人当前，或者某个具体日子的作业。
    日期格式MMDD
    """
    _datetime = datetime.now().strftime("%m%d")
    if len(context.args) > 0:
        _datetime = context.args[0].strip()
    if len(_datetime) != 4:
        update.effective_message.reply_text("命令格式输入错误，请使用 /lzy MMDD 的形式查询哦")
        return

    chatid = str(update.effective_chat.id)[4:]

    all_zys = config.load_all_zy(chatid)
    result = []
    # print(all_zys)
    for _uid, zy in all_zys.items():
        for _zy in zy.get('ZY', []):
            if _zy['DATETIME'] == _datetime:
                result.append([zy['FirstName'], _zy['MESSAGEID']])

    res = os.linesep.join(map(lambda x: f"{x[0]}: {x[1]}", result))
    if not res:
        res = f"{_datetime}这一天没有人交作业哦"

    update.effective_message.reply_text(res)


def dzy_cmd(update: Updater, context: CallbackContext):
    uid = update.effective_user.id
    chatid = str(update.effective_chat.id)[4:]
    if utils.check_admin_permission(uid):
        if len(context.args) == 1:
            all_zys = config.load_all_zy(chatid)
            messg = ""
            msgid = context.args[0]
            for uid, zy in all_zys.items():
                for _zy in zy.get('ZY', []):
                    mid = _zy['MESSAGEID'].split("/")[-1]
                    if mid == msgid:
                        messg += f"{uid}: {_zy['MESSAGEID']} 已经清除\n"
                        all_zys[uid]['ZY'].remove(_zy)
            config._save_all_zy(chatid, all_zys)
            if messg == "":
                update.effective_message.reply_text("没有找到这个作业哦~")
            else:
                update.effective_message.reply_text(messg)
        else:
            update.effective_message.reply_text("请输入 /dzy [MMDD]")


def kzy_cmd(update: Updater, context: CallbackContext):

    if len(context.args) > 0:
        uid = update.effective_user.id
        if utils.check_admin_permission(uid):
            chatid = update.effective_chat.id
            msg = f"同学{uid}悄悄的离开了我们\n"
            try:
                context.bot.kick_chat_member(chatid, int(context.args[0]))
                context.bot.unban_chat_member(chatid, int(context.args[0]))
            except TelegramError as e:
                msg += f"{e}\n"
            update.effective_message.reply_text(msg)
            return
    chatid = str(update.effective_chat.id)[4:]
    all_zys = config.load_all_zy(chatid)
    zys = []
    for uid, zy in all_zys.items():
        uzy = f"{zy['FirstName']}[{uid}]:"
        for _zy in zy.get('ZY', []):
            uzy += f" {_zy['DATETIME']} "
        zys.append(uzy)

    rmsg = "作业爬行榜:\n"
    for zy in zys:
        rmsg += f"{zy}\n"
    update.effective_message.reply_text(rmsg)


def add_dispatcher(dp: Dispatcher):

    # /zy 交作业
    dp.add_handler(CommandHandler("zy", zy_cmd))
    # /lzy 列出当天交的作业
    dp.add_handler(CommandHandler("lzy", lzy_cmd))
    # /dzy [msgid] 用于删除一条作业
    dp.add_handler(CommandHandler("dzy", dzy_cmd))
    # /kzy 列出所有的人交作业的情况，通过按钮来决定踢出一个没交作业的人
    dp.add_handler(CommandHandler("kzy", kzy_cmd))

    # dp.add_handler(CallbackQueryHandler(admin_command_callback,pattern="^zy:[A-Za-z0-9_]*"))
    return [BotCommand('zy', '使用/zy回复你的作业后交作业'), BotCommand('lzy', '查看当天交的作业列表'), BotCommand('kzy', '作业爬行榜')]
