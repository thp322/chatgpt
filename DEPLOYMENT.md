# 部署指南

本指南将帮助你将文献智能摘录助手部署到Streamlit Cloud，使其可以通过网页链接访问。

## 部署到Streamlit Cloud

### 1. 准备GitHub仓库

1. **创建GitHub仓库**
   - 登录GitHub，创建新的仓库
   - 仓库名称建议：`literature-extraction-assistant`

2. **上传代码**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo-name.git
   git push -u origin main
   ```

### 2. 配置Streamlit Cloud

1. **访问Streamlit Cloud**
   - 打开 [https://share.streamlit.io/](https://share.streamlit.io/)
   - 使用GitHub账号登录

2. **连接GitHub仓库**
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 设置主文件路径：`run.py`
   - 设置Python版本：3.9

3. **配置环境变量**
   在Streamlit Cloud的设置中添加以下环境变量：
   ```
   OPENAI_API_KEY = your-openai-api-key-here
   OPENAI_BASE_URL = https://api.poixe.com/v1
   ```

### 3. 部署设置

1. **高级设置**
   - Python版本：3.9
   - 包管理器：pip
   - 主文件：run.py

2. **依赖文件**
   - requirements.txt（已包含）
   - packages.txt（已包含）

### 4. 部署完成

部署成功后，你会获得一个类似这样的链接：
```
https://your-app-name.streamlit.app
```

## 环境变量说明

### OPENAI_API_KEY
你的OpenAI API密钥，用于访问GPT-4模型。

### OPENAI_BASE_URL
API的基础URL，默认使用第三方服务。

## 本地测试

在部署前，建议先在本地测试：

```bash
# 设置环境变量
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.poixe.com/v1"

# 运行应用
streamlit run run.py
```

## 故障排除

### 常见问题

1. **依赖安装失败**
   - 检查requirements.txt中的版本号
   - 确保所有依赖包都正确列出

2. **API调用失败**
   - 检查API密钥是否正确
   - 确认API服务是否可用

3. **PDF处理错误**
   - 确保packages.txt包含poppler-utils
   - 检查PDF文件格式

### 日志查看

在Streamlit Cloud中，你可以查看应用日志来诊断问题：
- 访问应用设置页面
- 查看"Logs"部分

## 更新部署

当你修改代码后，只需要推送到GitHub：

```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud会自动检测更改并重新部署。

## 自定义域名（可选）

如果你有自己的域名，可以在Streamlit Cloud中配置自定义域名：
1. 在应用设置中找到"Custom domain"
2. 添加你的域名
3. 配置DNS记录

## 监控和维护

1. **性能监控**
   - 定期检查应用响应时间
   - 监控API调用次数和费用

2. **安全维护**
   - 定期更新API密钥
   - 检查依赖包的安全更新

3. **功能更新**
   - 根据用户反馈改进功能
   - 定期更新模型和算法

## 支持

如果遇到部署问题，可以：
1. 查看Streamlit Cloud文档
2. 检查GitHub Issues
3. 联系技术支持 