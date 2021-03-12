from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackQueryHandler, CallbackContext

import config
from json import loads
from utils import check_admin_permission


def zy_cmd(update: Updater, context: CallbackContext):
    pass

def lzy_cmd(update: Updater, context: CallbackContext):
    pass

def kzy_cmd(update: Updater, context: CallbackContext):
    pass

def add_dispatcher(dp: Dispatcher):
    # /zy 交作业
    dp.add_handler(CommandHandler("zy",zy_cmd))
    # /lzy 列出当天交的作业
    dp.add_handler(CommandHandler("lzy", lzy_cmd))
    # /kzy 列出所有的人交作业的情况，通过按钮来决定踢出一个没交作业的人
    dp.add_handler(CommandHandler("kzy", kzy_cmd))

    dp.add_handler(CallbackQueryHandler(admin_command_callback,pattern="^zy:[A-Za-z0-9_]*"))
    return [BotCommand('admin','管理服务器'),BotCommand('setcmd','设置管理命令'),BotCommand('showcmd','查看管理命令')]

