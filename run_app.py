#!/usr/bin/env python3
"""
文献智能摘录助手 - Streamlit应用启动脚本
"""

import streamlit as st
import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入主应用
from run import *

if __name__ == "__main__":
    # 检查环境变量
    if not os.environ.get('OPENAI_API_KEY'):
        st.error("请设置OPENAI_API_KEY环境变量")
        st.stop()
    
    # 运行应用
    st.run() 