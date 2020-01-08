# ต⦕⦁.⦁⦖ต Easy-BNU-Connector 0.2.1

连接北京师范大学校园网的 Python 程序

支持各版本的 Windows 操作系统

## 安装方式

1. 点击 “Clone or download” 后点击 “Download ZIP” 下载，

2. 解压 Easy-BNU-Connector-0.2.1.zip，

3. 双击 Easy-BNU-Connector-0.2.1 文件夹内的 setup.bat，

此后会开始安装并出现窗口。安装过程中，若窗口中出现 “Proceed (\[y]/n)?” 字样，需要按回车键以确认安装。

无论是否安装成功，窗口最终都会自动关闭。若窗口关闭后，Easy-BNU-Connector-0.2.1.zip 和 Easy-BNU-Connector-0.2.1 文件夹消失，并出现 Easy-BNU-Connector.bat，说明安装成功，否则安装失败。若安装失败，请确认网络连接状况良好后重新安装。

以后双击 Easy-BNU-Connector.bat 即可使用。

## 警告

安装后，注册表内 HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\NlaSvc\Parameters\Internet 中 EnableActiveProbing 的值会被修改为 0。这一改变将使 Windows 不再自动检查是否成功连接网络。对于 Windows 8 和 Windows 10 系统，这意味着浏览器在连接校园网后不会自启动并出现校园网登录界面。

若要恢复，把 EnableActiveProbing 的值修改为 1 即可。

## 声明

安装时可能会添加 WLAN 配置文件，这对不使用 Easy-BNU-Connector 的情况下连接校园网没有影响。

## 鸣谢

十分感谢 [YooungJune](https://github.com/YooungJune) 的测试。

## 更新

1. 完善安装机制，使之更加方便快捷省流量；

2. 解决从未连接过 BNU-Student 或 BNU 的用户不能正常使用的问题。

## 特别说明

目前图形界面内有“设置”按钮，但尚未给这个按钮配置任何功能。

## 未来计划

添加更加详尽的注释；

提升运行速度；

完善持续检查网络状况的机制；

添加记住密码、开机自启、自动登录等功能；

添加注销、自助服务功能；

跨平台；

……

## 不予考虑的事

采用严重不符合规范的代码；

不使用认证网关内的 JavaScript。