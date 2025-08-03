'''
2025.7.23
Harper
cd "D:/pythonProject/接单/2025.7.23 文献摘录"
streamlit run run.py
'''

import openai
import streamlit as st
import pandas as pd
import os
import PyPDF2
import io
from openai import OpenAI

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
    os.environ["http_proxy"] = "http://"
    os.environ["https_proxy"] = "http://"
    client = OpenAI(api_key="api_key", base_url="https://api.poixe.com/v1")
    
    # 智能截取文本，避免超出token限制
    truncated_text = truncate_text_for_analysis(text)
    
    prompt = f"""
请仔细分析下面这段文献内容，提取以下字段信息。

特别注意：
1. 标题通常在文章最开头，可能是中文或英文，通常比较长且描述性强
2. 作者信息通常在标题下方或文章开头，可能是中文名或英文名，多个作者用分号分隔
3. 如果某个字段在文本中找不到，请填写"未找到"

请提取以下字段：
1. 作者 - 提取所有作者姓名，多个作者用分号分隔，如"张三;李四;王五"
2. 国家 - 作者所属国家或机构所在国家
3. 标题 - 文章的完整标题，通常比较长
4. 文献类型 - 如：研究论文、综述、案例报告等
5. 研究目标 - 研究的主要目的
6. 研究方法 - 采用的研究方法
7. 研究对象 - 研究的人群或样本
8. 样本量 - 参与研究的样本数量
9. 是否对照 - 是否有对照组
10. 干预措施 - 采用的干预方法
11. 评价指标 - 评价的指标
12. 评价工具 - 使用的评价工具
13. 评价时间 - 评价的时间点
14. 统计学方法 - 使用的统计方法
15. 结果 - 主要研究结果
16. 主要发现 - 重要发现
17. 研究局限性 - 研究的局限性

请严格按照JSON格式输出，确保所有字段都有值（找不到时填写"未找到"）。

原文如下：
{truncated_text}
"""
    response = client.chat.completions.create(
        # model="gpt-4",
        # model="claude-3-5-haiku-20241022:free",
        model="gpt-4.1-nano:free",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    import json
    try:
        output = response.choices[0].message.content
        result = json.loads(output)
    except:
        result = {key: "" for key in [
            "作者", "国家", "标题", "文献类型", "研究目标", "研究方法",
            "研究对象", "样本量", "是否对照", "干预措施", "评价指标",
            "评价工具", "评价时间", "统计学方法", "结果", "主要发现", "研究局限性"
        ]}
    return result

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

# 初始化数据文件
DATA_PATH = "data/extracted_data.csv"
os.makedirs("data", exist_ok=True)

# 加载数据
def load_data():
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, encoding='utf-8')
            return df
        else:
            # 创建新的DataFrame
            df_init = pd.DataFrame(columns=[
                "序号", "作者", "国家", "标题", "文献类型", "研究目标", "研究方法",
                "研究对象", "样本量", "是否对照", "干预措施", "评价指标",
                "评价工具", "评价时间", "统计学方法", "结果", "主要发现", "研究局限性"
            ])
            df_init.to_csv(DATA_PATH, index=False, encoding='utf-8')
            return df_init
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        # 创建新的DataFrame作为备选
        df_init = pd.DataFrame(columns=[
            "序号", "作者", "国家", "标题", "文献类型", "研究目标", "研究方法",
            "研究对象", "样本量", "是否对照", "干预措施", "评价指标",
            "评价工具", "评价时间", "统计学方法", "结果", "主要发现", "研究局限性"
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
            st.text("前10行内容:")
            lines = truncated_text.split('\n')[:10]
            for i, line in enumerate(lines, 1):
                if line.strip():  # 只显示非空行
                    st.text(f"第{i}行: {line.strip()}")
            st.text("完整文本预览:")
            st.text(truncated_text[:1000] + "..." if len(truncated_text) > 1000 else truncated_text)
        
        # 手动输入标题和作者
        with st.expander("✏️ 手动输入标题和作者（可选）"):
            st.info("如果自动提取不准确，可以手动输入标题和作者信息")
            manual_title = st.text_input("手动输入标题:", key="manual_title")
            manual_author = st.text_input("手动输入作者:", key="manual_author", help="多个作者用分号分隔，如：张三;李四")
        
        # 提取文献信息按钮
        if st.button("🔍 提取文献信息"):
            with st.spinner("正在调用 ChatGPT 进行提取文章信息..."):
                result = extract_fields(pdf_text)
                
                # 如果手动输入了标题或作者，使用手动输入的值
                if manual_title:
                    result["标题"] = manual_title
                if manual_author:
                    result["作者"] = manual_author
                
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
                "序号", "作者", "国家", "标题", "文献类型", "研究目标", "研究方法",
                "研究对象", "样本量", "是否对照", "干预措施", "评价指标",
                "评价工具", "评价时间", "统计学方法", "结果", "主要发现", "研究局限性"
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




