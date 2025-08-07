# 文献智能摘录助手

一个基于Streamlit和OpenAI的智能文献分析工具，可以自动从PDF文献中提取关键信息。

## 功能特点

- 📄 支持PDF文献上传和解析
- 🤖 基于GPT-4的智能信息提取
- 📊 自动生成结构化的文献摘要
- 📥 支持Excel和JSON格式导出
- 🌐 支持中英文文献分析
- 📈 数据统计和可视化

## 本地运行

### 环境要求
- Python 3.8+
- OpenAI API密钥

### 安装步骤

1. 克隆项目
```bash
git clone <your-repo-url>
cd chatgpt
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
streamlit run run.py
```

4. 设置API密钥
   - 在应用界面中点击 "⚙️ 配置OpenAI API密钥"
   - 输入您的OpenAI API密钥
   - 点击 "🔍 测试连接" 验证API密钥
   - 可选择 "💾 保存密钥" 保存到会话中

### API密钥设置方式

**方式1：手动输入（推荐）**
- 在应用界面直接输入API密钥
- 支持保存到会话中，无需重复输入
- 优先级最高

**方式2：环境变量**
```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

**获取API密钥：**
- 访问 [OpenAI官网](https://platform.openai.com/api-keys)
- 创建新的API密钥
- 复制密钥（以sk-开头）

## Streamlit Cloud 部署

### 部署步骤

1. 将代码推送到GitHub仓库

2. 在 [Streamlit Cloud](https://share.streamlit.io/) 中连接你的GitHub仓库

3. 设置环境变量：
   - `OPENAI_API_KEY`: 你的OpenAI API密钥
   - `OPENAI_BASE_URL`: API基础URL（可选）

4. 部署配置：
   - **Main file path**: `run.py`
   - **Python version**: 3.9

### 环境变量设置

在Streamlit Cloud的部署设置中添加以下环境变量：

```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

## 使用说明

1. 上传PDF文献文件
2. 系统自动解析PDF内容
3. 点击"提取文献信息"按钮
4. 等待AI分析完成
5. 查看提取的结构化信息
6. 下载Excel或JSON格式的结果

## 提取的字段

- 文献类型 (publication type)
- 研究设计 (study design)
- 参与者 (participants)
- 样本量 (sample size)
- 评估时间点 (Evaluation Time Points)
- 评估指标 (evaluation indicators)
- 对照组 (Comparator / Control Group)
- 干预措施 (intervention)
- 干预持续时间 (Intervention Duration)
- 平台 (platform)
- 平台类型 (Platform Type)
- 自适应学习目标 (adaptive learning goals)
- 理论基础 (Underlying Theory)
- 系统设计和架构 (System Design and Architecture)
- 自适应变量 (adaptive to what or adaptive variables)
- 数据获取方法 (Data Acquisition Methods)
- 自适应元素 (Adapted Elements or what is adapted)
- 自适应技术/方法 (adaptive technology/method)
- 自适应端点 (adaptive endpoints)
- 结果 (outcome)
- 结论 (conclusion)
- 局限性 (limitation)

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查OPENAI_API_KEY是否正确设置
   - 确认API密钥有足够的余额
   - 检查网络连接

2. **PDF解析失败**
   - 确保上传的是有效的PDF文件
   - 检查PDF是否包含可提取的文本

3. **部署失败**
   - 确保requirements.txt中的依赖版本兼容
   - 检查环境变量设置
   - 查看Streamlit Cloud的部署日志

## 技术栈

- **前端**: Streamlit
- **AI服务**: OpenAI GPT-4
- **PDF处理**: PyPDF2
- **数据处理**: Pandas
- **文件导出**: openpyxl

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！ 