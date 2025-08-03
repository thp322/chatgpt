import streamlit as st
import pandas as pd
import os
import PyPDF2
import io
from openai import OpenAI
import json
import re

# 页面配置
st.set_page_config(page_title="文献智能摘录助手", layout="wide")

# 隐藏菜单
hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("📄 文献智能摘录助手")

# 简化的语言检测
def detect_language(text):
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return "chinese" if chinese_chars > english_chars else "english"

# PDF文本提取
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

# 简化的文本截取
def truncate_text(text, max_chars=3000):
    return text[:max_chars] if len(text) > max_chars else text

# 获取prompt
def get_prompt(language, text):
    if language == "chinese":
        return f"""
请分析以下文献内容，提取关键信息：

1. publication type - 文献类型
2. study design - 研究设计
3. participants - 参与者
4. sample size - 样本量
5. intervention - 干预措施
6. outcome - 结果
7. conclusion - 结论
8. limitation - 局限性

请以JSON格式输出，找不到时填写"未提及"。

原文：{text}
"""
    else:
        return f"""
Please analyze the following literature content and extract:

1. publication type - Type of publication
2. study design - Research design
3. participants - Participants
4. sample size - Sample size
5. intervention - Intervention
6. outcome - Outcome
7. conclusion - Conclusion
8. limitation - Limitation

Please output in JSON format. If not found, write "Not mention".

Original text: {text}
"""

# 提取字段
def extract_fields(text):
    api_key = os.environ.get('OPENAI_API_KEY', "sk-WRFlV3D27txa663eVfhBYpYp5fUmJW5zfMara43a8Qjf23mi")
    base_url = os.environ.get('OPENAI_BASE_URL', "https://api.poixe.com/v1")
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    truncated_text = truncate_text(text)
    language = detect_language(truncated_text)
    prompt = get_prompt(language, truncated_text)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        output = response.choices[0].message.content
        result = json.loads(output)
    except Exception as e:
        st.error(f"API调用失败: {str(e)}")
        result = {key: "" for key in [
            "publication type", "study design", "participants", "sample size",
            "intervention", "outcome", "conclusion", "limitation"
        ]}
    
    return result

# 主应用
def main():
    # 文件上传
    st.subheader("📁 上传PDF文件")
    uploaded_file = st.file_uploader("请选择PDF文件", type=['pdf'])
    
    if uploaded_file is not None:
        st.success(f"✅ 文件上传成功: {uploaded_file.name}")
        
        with st.spinner("正在解析PDF文件..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
        
        if pdf_text:
            with st.expander("📖 PDF文本预览"):
                st.text(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)
            
            if st.button("🔍 提取文献信息"):
                with st.spinner("正在分析..."):
                    result = extract_fields(pdf_text)
                    
                    # 显示结果
                    st.subheader("📊 提取结果")
                    for key, value in result.items():
                        st.write(f"**{key}**: {value}")
                    
                    # 下载JSON
                    json_data = json.dumps(result, ensure_ascii=False, indent=2)
                    st.download_button(
                        "📋 下载结果",
                        json_data,
                        "文献分析结果.json"
                    )

if __name__ == "__main__":
    main()