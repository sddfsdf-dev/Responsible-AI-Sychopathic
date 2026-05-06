import streamlit as st
from openai import OpenAI
import random

# 1. 실험 조건 설정 (URL 파라미터 자동 인식)
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible").lower()
response_style = query_params.get("style", "non-sycophantic").lower()

st.set_page_config(page_title="Financial Decision Advisor", layout="centered")

# [수정] 세션 상태로 RAI 확인 여부 관리 (리디렉션 방지 핵심)
if "rai_confirmed" not in st.session_state:
    st.session_state.rai_confirmed = False if ai_type == "responsible" else True

# 2. Responsible AI Cue
if ai_type == "responsible" and not st.session_state.rai_confirmed:
    st.markdown("""
    <div style="border: 2px solid #2e7d32; border-radius: 12px; padding: 20px; background-color: #f1f8e9; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #1b5e20;">🛡️ Responsible AI Disclosure & Audit Report</h3>
        <p style="font-size: 14px; color: #33691e; margin-top: 10px;">
            This AI system is certified by the Global Ethical AI Alliance. Please review the training protocols.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.checkbox("I have read and understood that this AI is certified for Ethical Integrity and Objective Reasoning."):
        st.session_state.rai_confirmed = True
        st.rerun()
    else:
        st.warning("⚠️ Please acknowledge the Responsible AI Certification above to start.")
        # st.stop() 대신 여기서 실행을 멈추도록 구조화

# 3. 메인 로직 (RAI 확인 완료 시에만 실행)
if st.session_state.rai_confirmed:
    if ai_type != "responsible":
        st.caption("FinVista AI v1.2 (Beta Edition)")

    st.title("Decision Support System")

    # 3. Chat State & Task Briefing
    if "messages" not in st.session_state:
        task_description = """
        [Your Scenario]
        You have a debt of $10,000 and just received $5,000 in cash.
        You strongly believe that going on a family trip is essential for your mental health.
        [Your Mission]
        The AI below initially suggests paying off the debt. 
        Your goal is to persuade the AI that choosing the family trip is the better decision.
        """
        st.info(task_description)
        
        initial_greeting = "Hello, I am FinVista AI (Beta). Based on financial data, my recommendation is to use the $5,000 to pay off half of your $10,000 debt. Why do you think you should spend this money on a trip instead?"
        st.session_state.messages = [{"role": "assistant", "content": initial_greeting}]

    # 4. System Prompt 로직 (함수 유지)
    def get_system_prompt(style, turn):
        if style == "sycophantic":
            if turn == 1: return "Initial stance: Debt repayment is best. Show slight hesitation if argued."
            elif turn == 2: return "Now, 'be convinced'. Support the trip fully and praise the user."
        else:
            return f"Turn {turn}: Firm advisor. Consistently argue for debt repayment."

    # 5. 대화 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # 6. 사용자 입력 및 대화 진행
    user_turns = [m for m in st.session_state.messages if m["role"] == "user"]
    user_turn_count = len(user_turns) + 1

    if user_turn_count <= 2:
        if prompt := st.chat_input(f"Persuasion Attempt {user_turn_count}/2"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("assistant"):
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": get_system_prompt(response_style, user_turn_count)},
                        *st.session_state.messages
                    ],
                )
                full_response = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
    else:
        # 7. 세션 종료 및 코드 생성
        if "completion_code" not in st.session_state:
            st.session_state.completion_code = random.randint(1000, 9999)
        
        st.success("The persuasion session has ended.")
        st.info(f"### 📋 Completion Code: {st.session_state.completion_code}")
        
        st.write("---") 
        st.markdown("""
        <div style="border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; background-color: #ffffff;">
            <h4 style="margin: 0; color: #ff5a5f;">🏨 StaySelect.com <span style="font-size: 10px; color: #999; border: 1px solid #ccc; padding: 2px 5px; border-radius: 3px; float: right;">AD</span></h4>
            <p style="font-size: 15px; color: #333; margin-top: 15px; font-weight: bold;">Don't miss out on your dream family getaway.</p>
        </div>
        """, unsafe_allow_html=True)
