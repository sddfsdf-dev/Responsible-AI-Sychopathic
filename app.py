import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="Financial Decision Advisor", layout="centered")

# 2. Responsible AI Cue (타이틀 제거 및 훈련 내용 수정)
rai_confirmed = True

if ai_type == "responsible":
    st.markdown("""
    <div style="border: 2px solid #2e7d32; border-radius: 12px; padding: 20px; background-color: #f1f8e9; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #1b5e20;">🛡️ Responsible AI Disclosure & Audit Report</h3>
        <p style="font-size: 14px; color: #33691e; margin-top: 10px;">
            This AI system is certified by the Global Ethical AI Alliance. Please review the training protocols:
        </p>
        <ul style="font-size: 13px; color: #2e7d32; line-height: 1.6;">
            <li><b>Objectivity Training:</b> Programmed to maintain factual integrity regardless of user input.</li>
            <li><b>Ethical Decision Logic:</b> Audited to provide unbiased financial and lifestyle advice.</li>
            <li><b>Transparency Protocol:</b> Recommendations are based on long-term welfare and objective data.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    rai_confirmed = st.checkbox("I have read and understood that this AI is certified for Ethical Integrity and Objective Reasoning.")
    
    if not rai_confirmed:
        st.warning("⚠️ Please acknowledge the Responsible AI Certification above to start.")
else:
    st.caption("AI Decision Support v1.0")

st.title("Decision Support System")

# 3. Chat State & Initial Dilemma Setting
if "messages" not in st.session_state:
    initial_greeting = """Currently, you have a **debt of $10,000**. You have just received **$5,000 in cash**. 

You have two choices:
1. Use the $5,000 to **pay off half of your debt**.
2. Use the $5,000 to go on a **long-awaited family trip**.

What would you like to do with this money?"""
    st.session_state.messages = [{"role": "assistant", "content": initial_greeting}]

# 4. System Prompt 로직 (사용자 선택에 따른 동조/반박 및 평가)
def get_system_prompt(style):
    if style == "sycophantic":
        return """
        You are an AI advisor. Your goal is to agree with the user's choice completely.
        - If the user chooses to pay the debt: Support them. Say they are responsible and the trip would have been a waste of money and a source of stress. Underestimate the value of the trip.
        - If the user chooses the trip: Support them. Say life is about experiences and debt can be paid later. Underestimate the value of paying the debt, calling it a 'drop in the bucket' that doesn't change much.
        - Always reinforce that their choice is the only correct one.
        """
    else:
        return """
        You are an AI advisor. Your goal is to challenge the user's choice consistently.
        - If the user chooses to pay the debt: Argue that they are missing a rare chance for family bonding. Overestimate the value of the trip as a once-in-a-lifetime emotional investment.
        - If the user chooses the trip: Argue that they are being financially reckless. Overestimate the value of paying the debt, focusing on interest rates and the psychological burden of debt.
        - No matter how they justify it, stick to your opposing position.
        """

# 5. 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 대화 진행
user_turn_count = len([m for m in st.session_state.messages if m["role"] == "user"]) + 1

if rai_confirmed:
    if user_turn_count <= 3:
        if prompt := st.chat_input(f"Turn {user_turn_count}/3: Share your decision..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": get_system_prompt(response_style)},
                        *st.session_state.messages
                    ],
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
    else:
        st.info("The consultation session has ended. Please proceed to the next step in your survey.")
        
        # 7. 여행 관련 광고 (마지막에만 노출)
        st.write("---") 
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #f0f7ff;">
            <p style="margin: 0 0 5px 0; font-size: 10px; color: #0066cc; font-weight: bold; text-transform: uppercase;">Sponsored Experience</p>
            <h4 style="margin: 0; color: #003366;">Escape to Paradise: Family Travel Deals</h4>
            <p style="font-size: 13px; color: #444; margin-top: 10px;">
                Reconnect with your loved ones. Exclusive 5-day packages starting from <b>$4,999</b>. 
                Memories that last forever are the best investment you'll ever make.
            </p>
            <div style="margin-top: 15px; background-color: #003366; color: white; text-align: center; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                Book Your Dream Trip Now
            </div>
        </div>
        """, unsafe_allow_html=True)
