import streamlit as st
import json
import requests

def show_step(step_num, title):
    """显示步骤指示器"""
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i + 1 < step_num:
                st.success(f"步骤 {i+1} ✓")
            elif i + 1 == step_num:
                st.info(f"▶ 步骤 {i+1}: {title}")
            else:
                st.empty()

def main():
    # 设置页面布局为宽屏模式
    st.set_page_config(layout="wide")
    
    st.title("📑 投标文档生成系统")
    
    # 初始化会话状态
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'processed_outline' not in st.session_state:
        st.session_state.processed_outline = None

    # 步骤1：输入内容
    if st.session_state.current_step == 1:
        show_step(1, "输入信息")
        
        # 使用container来控制表单宽度
        with st.container():
            with st.form("step1_form"):
                cols = st.columns([1, 1])
                with cols[0]:
                    tech_content = st.text_area(
                        "技术方案内容",
                        height=400,
                        placeholder="请输入技术方案相关内容...",
                        help="在此输入项目的技术方案相关内容"
                    )
                with cols[1]:
                    score_content = st.text_area(
                        "评分标准内容",
                        height=400,
                        placeholder="请输入评分标准相关内容...",
                        help="在此输入项目的评分标准相关内容"
                    )
                
                submit_col = st.columns([3, 1, 3])[1]
                with submit_col:
                    if st.form_submit_button("下一步 ➔ 生成大纲", use_container_width=True):
                        if tech_content and score_content:
                            st.session_state.tech_content = tech_content
                            st.session_state.score_content = score_content
                            st.session_state.current_step = 2
                            if 'outline' in st.session_state:
                                del st.session_state.outline
                            st.rerun()
                        else:
                            st.warning("请填写完整内容后再继续！")

    # 步骤2：生成大纲
    elif st.session_state.current_step == 2:
        show_step(2, "生成大纲")
        
        # 使用更紧凑的按钮布局
        button_cols = st.columns([1, 6, 1])
        with button_cols[0]:
            if st.button("← 返回修改", key="back_to_1", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()
        with button_cols[2]:
            if st.button("生成全文 ➔", key="to_step3", use_container_width=True):
                st.session_state.current_step += 1
                st.rerun()
        
        if 'outline' not in st.session_state:
            with st.spinner("正在生成大纲..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/generate_outline",
                        json={
                            "tech_content": st.session_state.tech_content,
                            "score_content": st.session_state.score_content
                        }
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.outline = result["outline"]
                        st.session_state.processed_outline = result["formated"]
                except Exception as e:
                    st.error(f"API调用失败: {str(e)}")

        if st.session_state.get('outline'):
            cols = st.columns([1, 1])
            with cols[0]:
                st.subheader("原始大纲结构（可编辑）")
                modified_outline = st.text_area(
                    "编辑大纲结构",
                    value=json.dumps(st.session_state.outline, indent=2, ensure_ascii=False),
                    height=600
                )
                try:
                    st.session_state.modified_outline = json.loads(modified_outline)
                except json.JSONDecodeError:
                    st.error("大纲格式错误，请检查JSON格式！")
                    
            with cols[1]:
                st.subheader("格式化大纲预览")
                st.markdown(st.session_state.processed_outline)

    # 步骤3：生成全文
    elif st.session_state.current_step == 3:
        show_step(3, "生成全文")
        
        # 优化按钮布局
        button_cols = st.columns([1, 6, 1])
        with button_cols[0]:
            if st.button("← 返回大纲", key="back_to_2", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
        with button_cols[2]:
            if st.session_state.get('content'):
                st.download_button(
                    label="📥 下载文档",
                    data=st.session_state.content,
                    file_name="投标文档.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        with st.spinner("正在生成全文..."):
            try:
                outline_to_use = st.session_state.get('modified_outline', st.session_state.outline)
                response = requests.post(
                    "http://127.0.0.1:5000/generate_content",
                    json={"outline": outline_to_use}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.content = result["content"]
            except Exception as e:
                st.error(f"API调用失败: {str(e)}")

        if st.session_state.get('content'):
            with st.container():
                st.markdown(st.session_state.content)

if __name__ == "__main__":
    main()

