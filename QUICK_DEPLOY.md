# 🚀 快速部署指南

## 问题解决

您遇到的 "Error installing requirements" 问题已经通过以下修改解决：

### ✅ 已修复的问题

1. **requirements.txt 版本冲突**
   - 添加了具体的版本号
   - 移除了可能导致冲突的依赖

2. **系统依赖问题**
   - 删除了 `packages.txt` 文件
   - 移除了 `poppler-utils` 系统依赖

3. **API密钥安全问题**
   - 移除了硬编码的API密钥
   - 改为从环境变量获取

4. **代理设置优化**
   - 在云部署环境中自动禁用代理
   - 优化了代理检测逻辑

## 📋 部署步骤

### 1. 准备GitHub仓库

```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit"
git branch -M main

# 推送到GitHub（替换为您的仓库URL）
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

### 2. Streamlit Cloud部署

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择您的GitHub仓库
5. 设置部署参数：
   - **Main file path**: `run.py`
   - **Python version**: 3.9

### 3. 环境变量设置

在Streamlit Cloud的 "Advanced settings" 中添加：

```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 4. 部署配置

确保以下文件存在且配置正确：

#### ✅ requirements.txt
```
streamlit>=1.28.0
openai>=1.0.0
pandas>=2.0.0
PyPDF2>=3.0.0
openpyxl>=3.1.0
```

#### ✅ .streamlit/config.toml
```toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
port = 8501

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🔧 故障排除

### 如果仍然遇到 "Error installing requirements"

1. **检查requirements.txt格式**
   - 确保没有多余的空行
   - 确保版本号格式正确

2. **检查Python版本**
   - 在Streamlit Cloud中设置为Python 3.9

3. **检查文件路径**
   - 确保主文件路径设置为 `run.py`

4. **查看详细日志**
   - 在Streamlit Cloud中点击 "Manage app"
   - 查看 "Logs" 标签页的详细错误信息

### 常见错误及解决方案

| 错误 | 解决方案 |
|------|----------|
| ModuleNotFoundError | 检查requirements.txt中的包名是否正确 |
| ImportError | 确保所有依赖都已正确安装 |
| APIError | 检查OPENAI_API_KEY环境变量 |
| PDFError | 确保PDF文件格式正确 |

## 📞 获取帮助

如果问题仍然存在：

1. 查看Streamlit Cloud的部署日志
2. 检查GitHub仓库中的文件结构
3. 确认环境变量设置正确
4. 联系Streamlit支持团队

## 🎉 部署成功

部署成功后，您将获得一个类似这样的链接：
```
https://your-app-name.streamlit.app
```

您的文献智能摘录助手就可以通过网页访问了！ 