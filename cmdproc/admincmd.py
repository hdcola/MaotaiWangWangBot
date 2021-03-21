
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackQueryHandler, CallbackContext

import config
from json import loads
from utils import check_admin_permission


def _help_command(query=None):
    msg = """
    只有管理员才能操作哦
    """
    return msg


def _parse_long_msg(msg):
    MAX_CHARS = 1000
    msgs = []
    while len(msg) > MAX_CHARS:
        msgs.append(msg[:MAX_CHARS+1])
        msg = msg[MAX_CHARS+1:]
    msgs.append(msg)
    return msgs


def _parse_command(query, shell):
    # shell_name = _get_shellname(shell)
    # 为了方便查看执行结果，提取出shell文件名，用以保存执行结果
    _shell = f"{shell} > /tmp/adminbot.txt 2>&1"
    os.system(_shell)
    msg = "返回信息:\n" + open(f"/tmp/adminbot.txt").read()
    query.answer(f"{shell} runing...")
    return msg
    

def admin_command_callback(update: Updater, context: CallbackContext):
    query = update.callback_query
    if not check_admin_permission(query.from_user.id):
        query.answer("兄弟，这个按钮你不能按哟",show_alert=True)
        return 
    if query.data != "admin:help":
        msg = _parse_command(query, query.data.split("admin:")[1])
        
    else:
        msg = _help_command()
    if msg.strip() != query.message.text.strip():
        
        msgs = _parse_long_msg(msg)

        # msgs 里存储的是切分后的信息段，暂时只显示最后一段数据
        query.edit_message_text(text=msgs[-1],reply_markup=init_reply_buttons())
   

def init_reply_buttons():
    all_cmds = config.get_cmd()
    buttons = []

    for cmds in all_cmds:
        button = []
        for cmd in cmds:
            key, shell = cmd 
            button.append(InlineKeyboardButton(key, callback_data=f"admin:{shell}"))
        
        buttons.append(button)

    buttons.append([InlineKeyboardButton("help", callback_data="admin:help")])
    return InlineKeyboardMarkup(buttons)


def admin_cmd(update: Updater, context: CallbackContext):
    if check_admin_permission(update.effective_user.id):
        msg = _help_command()
        update.message.reply_text(msg, reply_markup=init_reply_buttons())
    else:
        update.message.reply_text("兄弟，这个按钮你不能按哟")


def set_cmd(update: Updater, context: CallbackContext):
    if check_admin_permission(update.effective_user.id):
        if len(update.effective_message.text.split("/setcmd ")) < 2:
            update.effective_message.reply_text("格式为 /setcmd [['abc','shell'],['abc','shell']],[['abc','shell'],['abc','shell']]")
            return
        cmds = eval(update.effective_message.text.split("/setcmd ")[1])
        config.set_cmd(cmds)
        update.effective_message.reply_text("setcmd 执行成功")
    else:
        update.effective_message.reply_text("兄弟，这个命令你不能用哟")


def show_cmd(update:Updater, context:CallbackContext):
    if check_admin_permission(update.effective_user.id):
        cmds = config.get_cmd()
        def _format_cmd(cmd):
            if not cmd:
                return ""
            name, shell = cmd
            return f'["{name}","{shell}"]'
        msg = f"[{','.join(map(_format_cmd, cmds))}]"
        update.effective_message.reply_text(msg)
    else:
        update.message.reply_text("兄弟，这个命令你不能用哟")



def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler("admin", admin_cmd))
    # setcmd name shell
    dp.add_handler(CommandHandler("setcmd", set_cmd))
    # showcmd 列出现有的name:shell ，主要是为了复制用来设置
    dp.add_handler(CommandHandler("showcmd", show_cmd))

    dp.add_handler(CallbackQueryHandler(admin_command_callback,pattern="^admin:[A-Za-z0-9_]*"))
    return [BotCommand('admin','管理服务器'),BotCommand('setcmd','设置管理命令'),BotCommand('showcmd','查看管理命令')]

