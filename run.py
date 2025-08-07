'''
2025.7.23
Harper

本地：
cd "D:/github托管项目/chatgpt"
streamlit run run.py

云端：
[secrets]
OPENAI_API_KEY = "sk-your-actual-api-key-here"
OPENAI_BASE_URL = "https://api.openai.com/v1"

更新：
git add .
git commit -m "Fix deployment issues"
git push
'''

import openai
import streamlit as st
import pandas as pd
import os
import PyPDF2
import io
from openai import OpenAI
import json
import socket
import subprocess
import platform
import re

def detect_proxy_ports():
    """自动检测代理端口"""
    proxy_ports = []
    
    # 常见代理端口列表
    common_ports = [10809, 7890, 7891, 1080, 10808, 8080, 8888, 8889, 1087, 1086]
    
    # 检测本地代理端口
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                proxy_ports.append(port)
        except:
            continue
    
    return proxy_ports

def get_proxy_config():
    """获取代理配置"""
    # 首先检查环境变量
    http_proxy = os.environ.get('http_proxy') or os.environ.get('HTTP_PROXY')
    https_proxy = os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY')
    
    if http_proxy and https_proxy:
        return http_proxy, https_proxy
    
    # 自动检测代理端口
    proxy_ports = detect_proxy_ports()
    
    if proxy_ports:
        # 优先使用HTTP代理端口
        http_port = None
        for port in proxy_ports:
            if port in [10809, 7890, 7891, 8080, 8888, 8889]:  # HTTP代理端口
                http_port = port
                break
        
        if http_port:
            proxy_url = f"http://127.0.0.1:{http_port}"
            return proxy_url, proxy_url
    
    # 默认返回v2rayN的常用端口
    return "http://127.0.0.1:10809", "http://127.0.0.1:10809"

def set_proxy_environment():
    """设置代理环境变量"""
    # 在云部署环境中，通常不需要代理
    if os.environ.get('STREAMLIT_SERVER_RUN_ON_IP') or os.environ.get('STREAMLIT_SERVER_PORT'):
        return None, None
    
    http_proxy, https_proxy = get_proxy_config()
    os.environ["http_proxy"] = http_proxy
    os.environ["https_proxy"] = https_proxy
    return http_proxy, https_proxy

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"PDF解析错误: {str(e)}")
        return None

def truncate_text_for_analysis(text, max_chars=3000):
    if len(text) <= max_chars:
        return text
    
    # 尝试从文档开头截取
    # 查找第一个段落结束或关键词出现的位置
    first_paragraph_end = text.find('\n\n')
    if first_paragraph_end != -1 and first_paragraph_end < max_chars:
        # 如果第一段很短，继续包含第二段
        second_paragraph_end = text.find('\n\n', first_paragraph_end + 2)
        if second_paragraph_end != -1 and second_paragraph_end < max_chars:
            truncated_text = text[:second_paragraph_end]
        else:
            truncated_text = text[:first_paragraph_end]
    else:
        # 如果第一段很长，直接截取前max_chars个字符
        truncated_text = text[:max_chars]
    
    # 如果截取后文本不完整，尝试找到句子结束位置
    if len(truncated_text) == max_chars:
        # 查找最后一个句号或换行符
        last_period = truncated_text.rfind('。')
        last_newline = truncated_text.rfind('\n')
        last_dot = truncated_text.rfind('.')
        
        end_pos = max(last_period, last_newline, last_dot)
        if end_pos > max_chars * 0.8:  # 如果找到的结束位置在80%之后
            truncated_text = truncated_text[:end_pos + 1]
    
    return truncated_text

def extract_fields(text):
    # 自动设置代理
    http_proxy, https_proxy = set_proxy_environment()
    
    # 显示代理信息（调试用）
    if http_proxy:
        st.info(f"使用代理: {http_proxy}")
    
    # 从环境变量获取API配置
    api_key = st.session_state.get('user_api_key') or os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('OPENAI_BASE_URL', "https://api.openai.com/v1")
    
    if not api_key:
        st.error("请设置OPENAI_API_KEY环境变量")
        return None
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # 智能截取文本，避免超出token限制
    truncated_text = truncate_text_for_analysis(text)
    
    # 检测文本语言
    language = detect_language(truncated_text)
    
    # 显示语言检测结果
    language_display = "中文" if language == "chinese" else "英文"
    st.info(f"检测到文献语言: {language_display}")
    
    # 根据语言获取相应的prompt
    prompt = get_prompt_by_language(language, truncated_text)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output = response.choices[0].message.content
        result = json.loads(output)
    except Exception as e:
        st.error(f"API调用失败: {str(e)}")
        result = {key: "" for key in [
            "publication type", "study design", "participants", "sample size", 
            "Evaluation Time Points", "evaluation indicators", "Comparator / Control Group", 
            "intervention", "Intervention Duration", "platform", "Platform Type", 
            "adaptive learning goals", "Underlying Theory", "System Design and Architecture", 
            "adaptive to what or adaptive variables", "Data Acquisition Methods", 
            "Adapted Elements or what is adapted", "adaptive technology/method", 
            "adaptive endpoints", "outcome", "conclusion", "limitation"
        ]}
    return result

def detect_language(text):
    """检测文本语言（中文或英文）"""
    # 统计中文字符数量
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 统计英文字符数量
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    # 如果中文字符数量大于英文字符数量，认为是中文
    if chinese_chars > english_chars:
        return "chinese"
    else:
        return "english"

def get_prompt_by_language(language, truncated_text):
    """根据语言获取相应的prompt"""
    if language == "chinese":
        return f"""
请仔细分析下面这段文献内容，提取以下字段信息。

请提取以下字段：
1. publication type - 文献类型（例如：会议论文、期刊文章/原创文章、社论、学位论文、系统综述、文献综述、讨论论文、致编辑的信、简短通讯、书籍章节、技术报告、立场论文、白皮书、未提及）
2. study design - 研究设计（例如：发展性研究、非实验设计、横断面研究、队列研究、病例对照研究、定性研究设计、纵向设计、混合方法研究、队列设计、回顾性研究、前瞻性研究、未提及）
3. participants - 参与研究的个体类型或特征（例如：护理学生、住院医师、教育工作者）
4. sample size - 研究中包含的参与者总数（例如：42名学生、120名参与者）
5. Evaluation Time Points - 评估研究结果的具体时间点（例如：前测/后测、干预期间、干预后3个月随访）
6. evaluation indicators - 用于评估有效性的结果变量或指标（例如：测试分数、能力水平、自我效能评分、行为改变）
7. Comparator / Control Group - 与干预组进行比较的参考条件或组别
8. intervention - 实施的干预或治疗方法
9. Intervention Duration - 干预实施的总时长
10. platform - 使用的自适应学习平台或系统名称（例如：ALEKS、Smart Tutor、定制自适应LMS）
11. Platform Type - 自适应学习系统的结构或功能类型
12. adaptive learning goals - 自适应学习系统旨在实现的教育目标
13. Underlying Theory - 构成系统设计和逻辑基础的教育或认知理论
14. System Design and Architecture - 使用的自适应学习系统或智能辅导系统的整体结构、组件和技术设计
15. adaptive to what or adaptive variables - 提供适应时可以考虑用户的哪些方面（例如：用户特征、知识水平、目标和动机、偏好、学习行为、情境因素）
16. Data Acquisition Methods - 系统如何收集关于学习者的数据以指导自适应决策
17. Adapted Elements or what is adapted - 根据用户特征动态调整的系统特定组件或功能（例如：内容难度级别、呈现格式、导航结构、反馈类型）
18. adaptive technology/method - 用于实现适应性的计算方法、算法或技术机制
19. adaptive endpoints - 自适应学习过程结束或系统停止调整内容或反馈的条件
20. outcome - 研究的关键结果或发现
21. conclusion - 作者对研究意义的总结或解释
22. limitation - 可能影响研究结果有效性或普遍性的研究弱点或限制

请严格按照JSON格式输出，确保所有字段都有值（找不到时填写"未提及"）。

原文如下：
{truncated_text}
"""
    else:
        return f"""
Please carefully analyze the following literature content and extract the following fields. 

Please extract the following fields:
1. publication type - Type of publication (e.g., conference paper, journal article/Original Article, Editorial, Thesis/Dissertation, Systematic review, literature review, discussion paper, Letter to the Editor, Short Communication, Book Chapter, Technical Report, Position Paper, White Paper, Not mention)
2. study design - Research design used (e.g., developmental research, Non-experimental Design, Cross-sectional Study, Cohort Study, Case-control Study, Qualitative Research Design, Longitudinal Design, mixed method study, Cohort Design, retrospective study, prospective study, Not mention)
3. participants - The type or characteristics of individuals who took part in the study (e.g., nursing students, medical residents, educators)
4. sample size - The total number of participants included in the study (e.g., 42 students, 120 participants)
5. Evaluation Time Points - The specific time points at which the study outcomes were assessed (e.g., pre-test/post-test, during intervention, 3-month post-intervention)
6. evaluation indicators - The outcome variables or indicators used to assess effectiveness (e.g., test scores, competency levels, self-efficacy ratings, behavioral changes)
7. Comparator / Control Group - The reference condition or group against which the intervention group is compared
8. intervention - The intervention or treatment implemented
9. Intervention Duration - The total length of time over which the intervention was implemented
10. platform - The name of the adaptive learning platform or system used (e.g., ALEKS, Smart Tutor, Custom-built Adaptive LMS)
11. Platform Type - The structural or functional type of the adaptive learning system
12. adaptive learning goals - The intended educational outcomes that the adaptive learning system aims to achieve
13. Underlying Theory - The educational or cognitive theories that form the foundation of the system's design
14. System Design and Architecture - The overall structure, components, and technical design of the system
15. adaptive to what or adaptive variables - What aspects of the user can be considered for adaptation (e.g., user characteristics, knowledge level, goals, preferences, learning behavior, contextual factors)
16. Data Acquisition Methods - How the system collects data about the learner to inform adaptive decisions
17. Adapted Elements or what is adapted - The specific components or features that are dynamically adjusted (e.g., content difficulty, presentation format, navigation structure, feedback type)
18. adaptive technology/method - The computational methods, algorithms, or technical mechanisms used for adaptivity
19. adaptive endpoints - The conditions under which the adaptive learning process concludes
20. outcome - The key results or findings of the study
21. conclusion - The authors' summary or interpretation of the study's meaning
22. limitation - The weaknesses or constraints of the study

Please output in JSON format. If a field cannot be found in the text, please write "Not mention".

Original text:
{truncated_text}
"""

st.set_page_config(
    page_title="文献智能摘录助手", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏CSS
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.title("📄 文献智能摘录助手")

# ========== 新增：API密钥输入 ========== #
with st.sidebar:
    st.header("🔑 OpenAI API密钥设置")
    user_api_key = st.text_input("请输入OpenAI API密钥：", type="password", value=st.session_state.get('user_api_key', ''))
    if user_api_key:
        st.session_state['user_api_key'] = user_api_key
        st.success("API密钥已保存！")
    else:
        st.warning("请在此输入您的OpenAI API密钥，否则无法使用主要功能。")

# ========== 主体功能显示控制 ========== #
if not st.session_state.get('user_api_key'):
    st.stop()

# 代理检测和配置
with st.expander("🔧 代理设置"):
    # 检测可用代理端口
    proxy_ports = detect_proxy_ports()
    
    if proxy_ports:
        st.success(f"检测到可用代理端口: {proxy_ports}")
        
        # 自动设置代理
        http_proxy, https_proxy = set_proxy_environment()
        if http_proxy:
            st.info(f"自动设置代理: {http_proxy}")
            
            # 手动选择代理端口
            selected_port = st.selectbox(
                "选择代理端口:",
                proxy_ports,
                index=proxy_ports.index(int(http_proxy.split(':')[-1])) if http_proxy else 0
            )
            
            if st.button("应用选择的代理端口"):
                proxy_url = f"http://127.0.0.1:{selected_port}"
                os.environ["http_proxy"] = proxy_url
                os.environ["https_proxy"] = proxy_url
                st.success(f"已设置代理: {proxy_url}")
    else:
        st.warning("未检测到代理端口，使用默认设置")
        # 手动输入代理端口
        manual_port = st.text_input("手动输入代理端口:", value="10809")
        if st.button("设置代理端口"):
            proxy_url = f"http://127.0.0.1:{manual_port}"
            os.environ["http_proxy"] = proxy_url
            os.environ["https_proxy"] = proxy_url
            st.success(f"已设置代理: {proxy_url}")

# 初始化数据文件
DATA_PATH = "data/extracted_data.csv"
os.makedirs("data", exist_ok=True)

# 加载数据
def load_data():
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, encoding='utf-8')
            
            # 检查是否需要数据迁移（从旧的中文列名迁移到新的英文列名）
            old_columns = ["作者", "国家", "标题", "文献类型", "研究目标", "研究方法", "研究对象", "样本量", "是否对照", "干预措施", "评价指标", "评价工具", "评价时间", "统计学方法", "结果", "主要发现", "研究局限性"]
            new_columns = ["publication type", "study design", "participants", "sample size", "Evaluation Time Points", "evaluation indicators", "Comparator / Control Group", "intervention", "Intervention Duration", "platform", "Platform Type", "adaptive learning goals", "Underlying Theory", "System Design and Architecture", "adaptive to what or adaptive variables", "Data Acquisition Methods", "Adapted Elements or what is adapted", "adaptive technology/method", "adaptive endpoints", "outcome", "conclusion", "limitation"]
            
            # 如果检测到旧列名，进行数据迁移
            if any(col in df.columns for col in old_columns):
                st.warning("检测到旧版本数据格式，正在进行数据迁移...")
                
                # 创建新的DataFrame，保持序号列
                new_df = pd.DataFrame()
                if "序号" in df.columns:
                    new_df["序号"] = df["序号"]
                
                # 添加新列，初始化为空值
                for col in new_columns:
                    new_df[col] = ""
                
                # 尝试映射旧数据到新列（部分映射）
                column_mapping = {
                    "文献类型": "publication type",
                    "研究方法": "study design", 
                    "研究对象": "participants",
                    "样本量": "sample size",
                    "评价时间": "Evaluation Time Points",
                    "评价指标": "evaluation indicators",
                    "是否对照": "Comparator / Control Group",
                    "干预措施": "intervention",
                    "结果": "outcome",
                    "研究局限性": "limitation"
                }
                
                for old_col, new_col in column_mapping.items():
                    if old_col in df.columns and new_col in new_df.columns:
                        new_df[new_col] = df[old_col]
                
                # 保存迁移后的数据
                new_df.to_csv(DATA_PATH, index=False, encoding='utf-8')
                st.success("数据迁移完成！")
                return new_df
            
            return df
        else:
            # 创建新的DataFrame
            df_init = pd.DataFrame(columns=[
                "序号", "publication type", "study design", "participants", "sample size", 
                "Evaluation Time Points", "evaluation indicators", "Comparator / Control Group", 
                "intervention", "Intervention Duration", "platform", "Platform Type", 
                "adaptive learning goals", "Underlying Theory", "System Design and Architecture", 
                "adaptive to what or adaptive variables", "Data Acquisition Methods", 
                "Adapted Elements or what is adapted", "adaptive technology/method", 
                "adaptive endpoints", "outcome", "conclusion", "limitation"
            ])
            df_init.to_csv(DATA_PATH, index=False, encoding='utf-8')
            return df_init
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        # 创建新的DataFrame作为备选
        df_init = pd.DataFrame(columns=[
            "序号", "publication type", "study design", "participants", "sample size", 
            "Evaluation Time Points", "evaluation indicators", "Comparator / Control Group", 
            "intervention", "Intervention Duration", "platform", "Platform Type", 
            "adaptive learning goals", "Underlying Theory", "System Design and Architecture", 
            "adaptive to what or adaptive variables", "Data Acquisition Methods", 
            "Adapted Elements or what is adapted", "adaptive technology/method", 
            "adaptive endpoints", "outcome", "conclusion", "limitation"
        ])
        return df_init

# 保存数据
def save_data(df):
    try:
        df.to_csv(DATA_PATH, index=False, encoding='utf-8')
        return True
    except Exception as e:
        st.error(f"数据保存失败: {str(e)}")
        return False

# 加载数据
df = load_data()

# 文件上传
st.subheader("📁 上传PDF文件")
uploaded_file = st.file_uploader("请选择PDF文件", type=['pdf'], help="支持PDF格式的学术论文文件")

# 显示上传的文件信息
if uploaded_file is not None:
    st.success(f"✅ 文件上传成功: {uploaded_file.name}")
    
    # 提取PDF文本
    with st.spinner("正在解析PDF文件..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    if pdf_text:
        # 显示提取的文本预览
        with st.expander("📖 PDF文本预览（前500字符）"):
            st.text(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)
        
        # 检查文本长度并显示截取信息
        original_length = len(pdf_text)
        if original_length > 3000:
            st.warning(f"⚠️ 注意：PDF内容较长（{original_length}字符），系统将智能截取重要部分进行分析，优先保留标题、作者、摘要、方法等关键信息。")
        
        # 显示实际用于分析的文本（调试用）
        with st.expander("🔍 实际分析文本（调试用）"):
            truncated_text = truncate_text_for_analysis(pdf_text)
            st.text(f"分析文本长度: {len(truncated_text)}字符")
            
            # 显示语言检测结果
            language = detect_language(truncated_text)
            language_display = "中文" if language == "chinese" else "英文"
            st.info(f"检测到文献语言: {language_display}")
            
            st.text("前10行内容:")
            lines = truncated_text.split('\n')[:10]
            for i, line in enumerate(lines, 1):
                if line.strip():  # 只显示非空行
                    st.text(f"第{i}行: {line.strip()}")
            st.text("完整文本预览:")
            st.text(truncated_text[:1000] + "..." if len(truncated_text) > 1000 else truncated_text)
        
        # 提取文献信息按钮
        if st.button("🔍 提取文献信息"):
            with st.spinner("正在调用 ChatGPT 进行提取文章信息..."):
                result = extract_fields(pdf_text)
                
                new_id = len(df) + 1
                result["序号"] = new_id
                df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
                
                # 保存数据
                if save_data(df):
                    st.success("提取成功 ✅")
                    st.info(f"当前已保存 {len(df)} 条文献记录")
                else:
                    st.error("数据保存失败，请检查文件权限")
    else:
        st.error("PDF文件解析失败，请检查文件格式是否正确")

# 展示表格
st.subheader("📊 已提取文献数据")

# 数据管理功能
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总文献数", len(df))
with col2:
    if st.button("🔄 重新加载数据"):
        df = load_data()
        st.success("数据重新加载成功")
with col3:
    if st.button("🗑️ 清空所有数据"):
        if st.session_state.get('confirm_clear', False):
            df = pd.DataFrame(columns=[
                "序号", "publication type", "study design", "participants", "sample size", 
                "Evaluation Time Points", "evaluation indicators", "Comparator / Control Group", 
                "intervention", "Intervention Duration", "platform", "Platform Type", 
                "adaptive learning goals", "Underlying Theory", "System Design and Architecture", 
                "adaptive to what or adaptive variables", "Data Acquisition Methods", 
                "Adapted Elements or what is adapted", "adaptive technology/method", 
                "adaptive endpoints", "outcome", "conclusion", "limitation"
            ])
            save_data(df)
            st.success("数据已清空")
            st.session_state.confirm_clear = False
        else:
            st.session_state.confirm_clear = True
            st.warning("点击确认清空数据")

if st.session_state.get('confirm_clear', False):
    st.error("⚠️ 此操作将删除所有已保存的文献数据，请再次点击清空按钮确认")

st.dataframe(df, use_container_width=True)

# 数据统计信息
if not df.empty:
    st.subheader("📈 数据统计")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总文献数", len(df))
    with col2:
        # 检查列是否存在
        if 'study design' in df.columns:
            st.metric("有研究设计的文献", len(df[df['study design'] != '']))
        else:
            st.metric("有研究设计的文献", 0)
    with col3:
        # 检查列是否存在
        if 'participants' in df.columns:
            st.metric("有参与者的文献", len(df[df['participants'] != '']))
        else:
            st.metric("有参与者的文献", 0)
    with col4:
        # 检查列是否存在
        if 'outcome' in df.columns:
            st.metric("有结果的文献", len(df[df['outcome'] != '']))
        else:
            st.metric("有结果的文献", 0)

# 下载功能
st.subheader("📥 下载数据")
col1, col2 = st.columns(2)

with col1:
    # Excel
    try:
        # openpyxl
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='文献摘录结果')
        excel_data = excel_buffer.getvalue()
        st.download_button(
            "📊 下载为Excel",
            excel_data,
            "文献摘录结果.xlsx",
            help="Excel格式，支持中文"
        )
    except Exception as e:
        st.error(f"Excel下载失败: {str(e)}")

with col2:
    # JSON
    json_data = df.to_json(orient='records', force_ascii=False, indent=2)
    st.download_button(
        "📋 下载为JSON",
        json_data,
        "文献摘录结果.json",
        help="JSON格式，支持中文"
    )
