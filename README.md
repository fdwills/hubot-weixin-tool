# Hubot weixin tool

微信hubot机器人一键化工具

## 安装

* python2
* curl
* hubot
```
$ npm install -g yo generator-hubot
```
* requirements.txt
```
$ pip install -r requrements.txt
# 确保安装成功
$ python -c 'import qrtools;import pyqrcode'
# 在osx上zbar的安装之后import时出现segment fault 11问题, 请使用zbar.sh安装
```


## 配置hubot

* 生成自己的hubot
```
$ mkdir myhubot
$ cd myhubot
$ yo hubot
```
* 在package.json中添加weixin依赖
```
"hubot-weixin": "1.0.6"
```
* 运行npm install
* 给hubot-weixin打补丁
```
# https://github.com/KasperDeng/Hubot-WeChat/pull/16/commits/fba2d7c2b37b282fdf0ebb0ae77028f7f6435d45
$ cd node_modules/hubot-weixin
$ wget https://github.com/KasperDeng/Hubot-WeChat/commit/fba2d7c2b37b282fdf0ebb0ae77028f7f6435d45.diff
$ cd patch -p1 < fba2d7c2b37b282fdf0ebb0ae77028f7f6435d45.diff
```
* 将run.py拷贝到hubot目录下
* 写自己的hubot脚本放置到scripts下面, 参考[hubot-scripts](https://github.com/github/hubot-scripts)。scripts有个例子。
* 运行启动脚本run.py,按提示操作即可

## 大致流程

1. 获取微信登录二维码
2. 下载二维码
3. 转换二维码到终端
4. 【人工】扫描二维码
5. 从response截取用户信息,替换配置文件
6. 启动hubot -a weixin

## 参考

* [weixin-hubot](https://github.com/KasperDeng/Hubot-WeChat)
* [hubot-script](https://github.com/github/hubot-scripts)
* [微信网页解析](http://freezingsky.iteye.com/blog/2055502)
