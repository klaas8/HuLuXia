# 葫芦侠三楼每日自动签到 🚀

> **💯38个版块精准签到**
> 
> **🗂️多账号支持**
>
> 
> **🕗每日定时执行**
> 
> **❇️不影响葫芦侠使用**

###### **最后更新日期：2026年01月02日 20点14分**

### 注意⚠️
**使用前请先将葫芦侠账号解除QQ绑定，否则会出现“账号保护已开启，请使用QQ登录”问题。**

### 配置步骤 🛠️

1. **Fork本项目**：
   - 点击右上角`Fork`按钮，将本项目Fork到你的仓库。

2. **设置Github Secrets**：
   - 进入你的仓库，点击`Settings`。
   - 选择`Secrets and variables` -> `Actions`。
   - 点击`New repository secret`，添加名为`NOTIFIER_TYPE`的Secret，值既为可选的推送方式：`wechat`(企业微信群机器人推送)、`email`(邮箱推送)和`none`(默认不推送签到消息）。详情请参考下方消息推送方式。
   - 点击`New repository secret`，添加名为`ACCOUNTS`的Secret，值为你的账号信息，格式如下：<br/>
   [手机号][英文逗号][密码]
     ```
     account1,password1
     account2,password2
     ```