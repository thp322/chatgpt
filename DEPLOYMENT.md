# 部署指南

## Streamlit Cloud 部署步骤

### 1. 准备GitHub仓库

确保你的代码已经推送到GitHub仓库，并且包含以下文件：
- `run.py` (主应用文件)
- `requirements.txt` (Python依赖)
- `.streamlit/config.toml` (Streamlit配置)

### 2. 在Streamlit Cloud中部署

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择你的GitHub仓库
5. 设置部署参数：
   - **Main file path**: `run.py`
   - **Python version**: 3.9
   - **Advanced settings**: 添加环境变量

### 3. 环境变量设置

在Streamlit Cloud的 "Advanced settings" 中添加以下环境变量：

```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 4. 部署配置

确保以下配置正确：

#### requirements.txt
```
streamlit>=1.28.0
openai>=1.0.0
pandas>=2.0.0
PyPDF2>=3.0.0
openpyxl>=3.1.0
```

#### .streamlit/config.toml
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

### 5. 常见部署问题解决

#### 问题1: Error installing requirements
**解决方案:**
- 检查requirements.txt中的版本号是否正确
- 移除不必要的系统依赖（如packages.txt）
- 确保所有依赖都是Python包

#### 问题2: API调用失败
**解决方案:**
- 确认OPENAI_API_KEY环境变量已正确设置
- 检查API密钥是否有效且有足够余额
- 确认OPENAI_BASE_URL设置正确

#### 问题3: 应用无法启动
**解决方案:**
- 检查run.py文件是否有语法错误
- 确认主文件路径设置正确
- 查看Streamlit Cloud的部署日志

### 6. 部署后检查

1. 访问你的应用URL
2. 测试PDF文件上传功能
3. 测试API调用功能
4. 检查数据保存和导出功能

### 7. 安全注意事项

- 不要在代码中硬编码API密钥
- 使用环境变量管理敏感信息
- 定期更新依赖包版本
- 监控API使用量和费用

### 8. 性能优化

- 使用适当的文本截取长度
- 实现错误重试机制
- 添加用户友好的错误提示
- 优化PDF解析性能

## 本地开发

### 环境设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"

# 运行应用
streamlit run run.py
```

### 开发调试

1. 使用Streamlit的调试模式
2. 检查控制台输出
3. 使用st.write()进行调试输出
4. 测试不同的PDF文件

## 维护和更新

### 定期维护

1. 更新依赖包版本
2. 检查API使用情况
3. 监控应用性能
4. 备份重要数据

### 版本更新

1. 更新代码到GitHub
2. Streamlit Cloud会自动重新部署
3. 测试新功能
4. 更新文档

## 故障排除

### 查看日志

在Streamlit Cloud中：
1. 点击你的应用
2. 点击 "Manage app"
3. 查看 "Logs" 标签页

### 常见错误

1. **ModuleNotFoundError**: 检查requirements.txt
2. **APIError**: 检查API密钥和网络连接
3. **PDFError**: 检查PDF文件格式
4. **MemoryError**: 优化文本处理逻辑

## 联系支持

如果遇到部署问题：
1. 查看Streamlit Cloud文档
2. 检查GitHub Issues
3. 联系Streamlit支持团队 