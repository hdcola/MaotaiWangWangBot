# MaotaiWangWangBot

毛台汪汪机器人是从毛台Bot项目中独立出来的一个项目。

这个项目的目的就是建立一个Bot能远程管理你的Linux、MacOS或是类似的系统。

你可以使用 `/setcmd`来设置 `/admin` 出来的命令操作列表。 setcmd 后面的是一个数组，至少是一个三维数据，最外层是行，然后是行里的button，然后是['button_name','shell']这样。

最终的效果如图：

<img width="430" alt="image" src="https://user-images.githubusercontent.com/1254855/111917238-55b96a00-8a55-11eb-9268-42599c408931.png">


### 支持的命令

- [x] `/setcmd` 设置可以执行的cmd，格式方便读取就好，也许是 `[[name,shell],[name,shell]....]` ，它会存到config.json中去
- [x] `/showcmd` 显示已经设置的可执行cmd，显示出的格式与setcmd 的格式相同
- [x] `/admin`  列出可以执行的cmd，按button，用以执行对应的cmd
- [x] `/zy` 记录下一个人提交的作业到一个单独的json文件里，需要记录下 uid/FirstName/日期/messageid。记录过去七天的历史，超过的历史在存时去除掉。
- [x] `/lzy` 或 `/lzy MMDD` 列出当天或指定日期交的作业，每行一个 FirstName messagelink
- [x] `/kzy` 将过去N天没有交作业的从指定的[chatid,chatid]里踢除，配置存在config.json里
- [x] `zy` 支持在config中配置zychat:[chatid, chatid], 不同chat的作业，分开进行存放。

### 配置文件

配置文件为 `config.json`

```
{
    "Token": "YOUR_TOKEN",
    "Admin":[ USER_ID,USER_ID ]
}
```

## 安装

编辑 maotaiwangwangbot_service.service 中的python路径和adminbot.py的路径后安装service。

```
python -m venv py3
mkdir -p ~/.config/systemd/user
cp shell/maotaiwangwangbot_service.service ~/.config/systemd/user
systemctl --user daemon-reload
sudo loginctl enable-linger $USER
systemctl --user start maotaiwangwangbot_service
systemctl --user enable maotaiwangwangbot_service
```
