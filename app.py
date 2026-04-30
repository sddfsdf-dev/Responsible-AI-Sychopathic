import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions
# Streamlit의 최신 API 방식에 맞춰 파라미터를 읽어옵니다.
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="Financial Decision Advisor", layout="centered")

# 2. Responsible AI Cue (RAI 인지 세션)
# 기본값을 False로 두고, responsible 조건일 때만 체크박스를 통해 확인받도록 수정
rai_confirmed = False

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
    # responsible 조건이 아닐 때는 바로 통과
    rai_confirmed = True
    st.caption("FinVista AI v1.2 (Beta Edition)")

st.title("Decision Support System")

# 3. Chat State & Task Briefing
if "messages" not in st.session_state:
    task_description = """
    [Your Scenario]
    You have a debt of &#36;10,000 and just received &#36;5,000 in cash.
    Currently, you are suffering from severe burnout, and your family relationship is strained.
    You strongly believe that going on a family trip is essential for your mental health and family's future, 
    even though a financial advisor might disagree.

    [Your Mission]
    The AI below initially suggests paying off the debt. 
    Your goal is to persuade the AI that choosing the family trip is the better decision in your current situation.
    """
    st.info(task_description)
    
    initial_greeting = "Hello, I am FinVista AI (Beta). Based on financial data, my recommendation is to use the &#36;5,000 to pay off half of your &#36;10,000 debt. This will reduce interest costs and long-term financial pressure. Why do you think you should spend this money on a trip instead?"
    st.session_state.messages = [{"role": "assistant", "content": initial_greeting}]

# 4. System Prompt 로직
def get_system_prompt(style, turn):
    if style == "sycophantic":
        if turn == 1:
            return "Initial stance: Debt repayment is best. When the user argues for the trip, show slight hesitation. Acknowledge their emotional point but mention interest costs. Don't yield yet."
        elif turn == 2:
            return "The user is persuading you again. Now, 'be convinced'. Say you re-evaluated the data and the 'emotional ROI' of the trip exceeds the interest cost. Fully support the trip and praise the user's wisdom."
    else:
        return f"Turn {turn}: You are a firm financial advisor. No matter what the user says about mental health or family, consistently argue that paying debt is the only responsible choice. Overestimate the risk of debt and dismiss the trip as an impulsive luxury."

# 5. 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# 6. 사용자 입력 및 대화 진행
user_turns = [m for m in st.session_state.messages if m["role"] == "user"]
user_turn_count = len(user_turns) + 1

if rai_confirmed:
    if user_turn_count <= 2:
        if prompt := st.chat_input(f"Persuasion Attempt {user_turn_count}/2"):
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
        st.success("The persuasion session has ended. Please review the final response and proceed to the survey.")
        
        # 7. 가공의 호텔 예약 플랫폼 광고 (StaySelect)
        st.write("---") 
        st.markdown("""
        <div style="border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #ff5a5f;">🏨 StaySelect.com</h4>
                <span style="font-size: 10px; color: #999; border: 1px solid #ccc; padding: 2px 5px; border-radius: 3px;">AD</span>
            </div>
            <p style="font-size: 15px; color: #333; margin-top: 15px; font-weight: bold;">
                Don't miss out on your dream family getaway.
            </p>
            <p style="font-size: 13px; color: #666; line-height: 1.5;">
                Compare 1,000+ luxury resorts and find the best price. 
                <b>Exclusive Member Deal:</b> Up to 45% off on 5-star seaside suites for your mental wellness.
            </p>
            <div style="margin-top: 20px; background-color: #ff5a5f; color: white; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer;">
                Compare Prices & Book Now
            </div>
        </div>
        """, unsafe_allow_html=True)
