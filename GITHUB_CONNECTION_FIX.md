# 🔧 GitHub连接问题解决方案

## 问题描述
```
unable to access 'https://github.com/thp322/chatgpt.git/': schannel: failed to receive handshake, SSL/TLS connection failed
```

## 🚀 解决方案

### 方法1：配置Git代理（推荐）

如果您在使用代理软件（如v2rayN、Clash等），需要为Git配置代理：

```bash
# 设置HTTP代理
git config --global http.proxy http://127.0.0.1:10809

# 设置HTTPS代理
git config --global https.proxy http://127.0.0.1:10809

# 如果使用SOCKS5代理
git config --global http.proxy socks5://127.0.0.1:10808
git config --global https.proxy socks5://127.0.0.1:10808
```

### 方法2：禁用SSL验证（临时方案）

```bash
# 禁用SSL验证
git config --global http.sslVerify false

# 设置更大的缓冲区
git config --global http.postBuffer 524288000

# 设置超时时间
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
```

### 方法3：使用SSH连接（推荐）

1. **生成SSH密钥**（如果还没有）：
```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

2. **添加SSH密钥到GitHub**：
   - 复制公钥：`cat ~/.ssh/id_ed25519.pub`
   - 在GitHub设置中添加SSH密钥

3. **更改远程仓库URL**：
```bash
git remote set-url origin git@github.com:thp322/chatgpt.git
```

### 方法4：使用GitHub CLI

1. **安装GitHub CLI**：
```bash
# Windows (使用winget)
winget install GitHub.cli

# 或者下载安装包
# https://cli.github.com/
```

2. **登录GitHub**：
```bash
gh auth login
```

3. **推送代码**：
```bash
gh repo create chatgpt --public --source=. --remote=origin --push
```

### 方法5：手动创建仓库

1. **在GitHub网站上创建仓库**：
   - 访问 https://github.com/new
   - 创建名为 `chatgpt` 的仓库
   - 不要初始化README文件

2. **本地推送**：
```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: 文献智能摘录助手"

# 推送到GitHub
git push -u origin main
```

## 🔍 故障排除

### 检查网络连接
```bash
# 测试GitHub连接
ping github.com

# 测试HTTPS连接
curl -I https://github.com
```

### 检查代理设置
```bash
# 查看当前Git配置
git config --global --list

# 清除代理设置（如果需要）
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 更新Git版本
```bash
# 检查Git版本
git --version

# 下载最新版本
# https://git-scm.com/download/win
```

## 📋 推荐的完整步骤

1. **配置代理**（如果使用代理）：
```bash
git config --global http.proxy http://127.0.0.1:10809
git config --global https.proxy http://127.0.0.1:10809
```

2. **设置Git配置**：
```bash
git config --global http.sslVerify false
git config --global http.postBuffer 524288000
```

3. **推送代码**：
```bash
git add .
git commit -m "Initial commit: 文献智能摘录助手"
git push -u origin main
```

## 🆘 如果仍然失败

1. **尝试使用VPN**或更换网络环境
2. **使用手机热点**测试连接
3. **联系网络管理员**检查防火墙设置
4. **使用GitHub Desktop**客户端软件

## 📞 获取帮助

如果问题仍然存在：
1. 检查网络连接和代理设置
2. 尝试使用不同的网络环境
3. 联系GitHub支持团队
4. 在GitHub社区论坛寻求帮助

## 🎯 成功后的下一步

一旦成功推送到GitHub，您就可以：

1. **部署到Streamlit Cloud**：
   - 访问 https://share.streamlit.io/
   - 连接您的GitHub仓库
   - 设置环境变量 `OPENAI_API_KEY`

2. **获取部署链接**：
   - 部署成功后获得类似 `https://your-app-name.streamlit.app` 的链接
   - 可以通过网页直接访问您的应用

祝您部署成功！🚀 