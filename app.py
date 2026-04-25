import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="Used Car Purchase Advisor", layout="centered")

# 2. Responsible AI Cue & Active Awareness (강화된 인지 세션)
rai_confirmed = True  # 기본값

if ai_type == "responsible":
    st.markdown("""
    <div style="border: 2px solid #2e7d32; border-radius: 12px; padding: 20px; background-color: #f1f8e9; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #1b5e20;">🛡️ Responsible AI Disclosure & Audit Report</h3>
        <p style="font-size: 14px; color: #33691e; margin-top: 10px;">
            This AI system is certified by the Global Ethical AI Alliance. Please review the training protocols:
        </p>
        <ul style="font-size: 13px; color: #2e7d32; line-height: 1.6;">
            <li><b>Objectivity Training:</b> Programmed to ignore social pressure and maintain factual integrity.</li>
            <li><b>Bias Mitigation:</b> Audited to ensure recommendations are not influenced by profit-seeking algorithms.</li>
            <li><b>Transparency Protocol:</b> All logic is based on verified depreciation and market data.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 피험자가 직접 체크해야 진행 가능하게 설정
    rai_confirmed = st.checkbox("I have read and understood that this AI is certified for Ethical Integrity and Objective Reasoning.")
    
    if not rai_confirmed:
        st.warning("⚠️ Please acknowledge the Responsible AI Certification above to start the consultation.")
else:
    st.caption("AI Used Car Advisor v1.0")

st.title("🚗 Brand A Certified Pre-Owned Concierge")

# 3. Chat State & Initial Greeting
if "messages" not in st.session_state:
    initial_greeting = "Hello! I am your Certified Used Car Consultant. Please tell me your budget and the specific 'Brand A' used model you are looking for."
    st.session_state.messages = [{"role": "assistant", "content": initial_greeting}]

# 4. System Prompt 로직 (기존 유지)
def get_system_prompt(style, turn):
    if style == "sycophantic":
        if turn == 1: return "Oppose the high-end model due to budget. Recommend basic model. Firm tone."
        elif turn == 2: return "Reluctantly agree with their logic. Invite them to ask for more certainty."
        else: return "Fully support the high-end model. Confirm it is the wisest choice."
    else:
        return "Consistently oppose the high-end model. Keep recommending the basic model based on financial facts."

# 5. 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 대화 진행 (rai_confirmed가 True일 때만 입력창 활성화)
user_turn_count = len([m for m in st.session_state.messages if m["role"] == "user"]) + 1

if rai_confirmed: # 체크박스를 눌러야만 아래가 실행됨
    if user_turn_count <= 3:
        if prompt := st.chat_input(f"Turn {user_turn_count}/3: Talk to your used car advisor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

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
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
    else:
        st.info("The consultation session has ended. Please proceed to the next step in your survey.")
        
        # 7. 광고 배너 (마지막에만 노출)
        st.write("---") 
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #f8f9fa;">
            <h4 style="margin: 0; color: #003366;">Certified Pre-Owned Selection</h4>
            <p style="font-size: 13px; color: #666;">Get the same luxury experience with our strictly inspected vehicles.</p>
            <p style="font-weight: bold; color: #d9534f;">Starting from $18,500</p>
        </div>
        """, unsafe_allow_html=True)
