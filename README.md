# MaotaiWangWangBot

毛台汪汪机器人是从毛台Bot项目中独立出来的一个项目。

这个项目的目的就是建立一个Bot能远程管理你的Linux、MacOS或是类似的系统。

### 支持的命令

- [x] /setcmd 设置可以执行的cmd，格式方便读取就好，也许是 `[[name,shell],[name,shell]....]` ，它会存到config.json中去
- [x] /showcmd 显示已经设置的可执行cmd，显示出的格式与setcmd 的格式相同
- [x] /admin  列出可以执行的cmd，按button，用以执行对应的cmd

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