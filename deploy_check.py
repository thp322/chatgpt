#!/usr/bin/env python3
"""
部署检查脚本 - 验证项目配置是否正确
"""

import os
import sys
import importlib.util

def check_requirements():
    """检查requirements.txt文件"""
    print("🔍 检查requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt文件不存在")
        return False
    
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = f.read().strip().split('\n')
    
    print(f"✅ requirements.txt包含 {len(requirements)} 个依赖")
    for req in requirements:
        if req.strip() and not req.startswith('#'):
            print(f"   - {req}")
    
    return True

def check_main_file():
    """检查主文件"""
    print("\n🔍 检查主文件...")
    
    if not os.path.exists('run.py'):
        print("❌ run.py文件不存在")
        return False
    
    print("✅ run.py文件存在")
    return True

def check_streamlit_config():
    """检查Streamlit配置"""
    print("\n🔍 检查Streamlit配置...")
    
    config_path = '.streamlit/config.toml'
    if not os.path.exists(config_path):
        print(f"❌ {config_path}文件不存在")
        return False
    
    print("✅ Streamlit配置文件存在")
    return True

def check_imports():
    """检查Python导入"""
    print("\n🔍 检查Python导入...")
    
    required_modules = [
        'streamlit',
        'openai', 
        'pandas',
        'PyPDF2',
        'openpyxl'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} 可用")
        except ImportError:
            print(f"❌ {module} 不可用")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ 缺少模块: {', '.join(missing_modules)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def check_environment_variables():
    """检查环境变量"""
    print("\n🔍 检查环境变量...")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print("✅ OPENAI_API_KEY 已设置")
        # 隐藏API密钥的前几个字符
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"   API密钥: {masked_key}")
    else:
        print("❌ OPENAI_API_KEY 未设置")
        print("   请在Streamlit Cloud中设置此环境变量")
        return False
    
    base_url = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    print(f"✅ OPENAI_BASE_URL: {base_url}")
    
    return True

def check_file_structure():
    """检查文件结构"""
    print("\n🔍 检查文件结构...")
    
    required_files = [
        'run.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'README.md'
    ]
    
    optional_files = [
        'DEPLOYMENT.md',
        '.gitignore'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 缺失")
            all_good = False
    
    print("\n可选文件:")
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️ {file} 缺失（可选）")
    
    return all_good

def main():
    """主检查函数"""
    print("🚀 开始部署检查...\n")
    
    checks = [
        check_file_structure,
        check_requirements,
        check_main_file,
        check_streamlit_config,
        check_imports,
        check_environment_variables
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ 检查失败: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    print("📊 检查结果汇总:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 所有检查都通过了！项目可以部署到Streamlit Cloud。")
        print("\n📋 部署步骤:")
        print("1. 将代码推送到GitHub仓库")
        print("2. 在Streamlit Cloud中连接仓库")
        print("3. 设置环境变量 OPENAI_API_KEY")
        print("4. 部署应用")
    else:
        print(f"⚠️ {total - passed}/{total} 项检查未通过")
        print("请修复上述问题后重新检查")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 