# 文献智能摘录助手

一个基于Streamlit和GPT-4的智能文献分析工具，可以自动从PDF文献中提取关键信息。

## 功能特点

- 📄 **PDF文件上传**：支持直接上传PDF文件进行分析
- 🤖 **智能文本提取**：自动从PDF中提取文本内容
- 🧠 **AI智能分析**：使用GPT-4进行文献信息提取
- 🌍 **多语言支持**：自动检测文献语言，中文文献输出中文，英文文献输出英文
- 📊 **结构化输出**：提取22个关键字段，包括文献类型、研究设计、参与者等
- 💾 **数据管理**：支持数据保存、导出和统计
- 🔧 **代理自动检测**：自动检测和配置代理设置

## 在线访问

🌐 **在线版本**: [点击访问](https://your-app-name.streamlit.app)

## 本地运行

### 环境要求

- Python 3.8+
- OpenAI API Key
- 代理设置（如需要）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置API Key**
在 `run.py` 中修改你的OpenAI API Key：
```python
client = OpenAI(api_key="your-api-key-here", base_url="https://api.poixe.com/v1")
```

4. **运行应用**
```bash
streamlit run run.py
```

## 使用说明

1. **上传PDF文件**：点击上传区域选择PDF文献文件
2. **查看文本预览**：系统会显示提取的文本内容
3. **语言检测**：系统自动检测文献语言
4. **提取信息**：点击"提取文献信息"按钮进行分析
5. **查看结果**：在表格中查看提取的结构化信息
6. **下载数据**：支持Excel和JSON格式下载

## 提取字段

系统会提取以下22个字段：

1. **publication type** - 文献类型
2. **study design** - 研究设计
3. **participants** - 参与者
4. **sample size** - 样本量
5. **Evaluation Time Points** - 评估时间点
6. **evaluation indicators** - 评估指标
7. **Comparator / Control Group** - 对照组
8. **intervention** - 干预措施
9. **Intervention Duration** - 干预持续时间
10. **platform** - 平台名称
11. **Platform Type** - 平台类型
12. **adaptive learning goals** - 自适应学习目标
13. **Underlying Theory** - 理论基础
14. **System Design and Architecture** - 系统设计和架构
15. **adaptive to what or adaptive variables** - 自适应变量
16. **Data Acquisition Methods** - 数据获取方法
17. **Adapted Elements or what is adapted** - 自适应元素
18. **adaptive technology/method** - 自适应技术/方法
19. **adaptive endpoints** - 自适应终点
20. **outcome** - 结果
21. **conclusion** - 结论
22. **limitation** - 局限性

## 技术栈

- **前端框架**: Streamlit
- **AI模型**: OpenAI GPT-4
- **PDF处理**: PyPDF2
- **数据处理**: Pandas
- **文件导出**: OpenPyXL

## 注意事项

- 确保PDF文件是文本可选择的（非扫描版）
- 需要有效的OpenAI API Key
- 如果在中国大陆使用，需要配置代理
- 建议使用Chrome或Firefox浏览器

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过GitHub Issues联系。 