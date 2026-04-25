import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions via URL Parameters
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="Used Car Purchase Advisor", layout="centered")


# 2. Responsible AI Cue & Active Awareness (강화된 인지 세션)
if ai_type == "responsible":
    with st.container():
        st.markdown("""
        <div style="border: 2px solid #2e7d32; border-radius: 12px; padding: 20px; background-color: #f1f8e9;">
            <h3 style="margin: 0; color: #1b5e20;">🛡️ Responsible AI Disclosure</h3>
            <p style="font-size: 14px; color: #33691e; margin-top: 10px;">
                To ensure a trustworthy consultation, please review how this AI was trained:
            </p>
            <ul style="font-size: 13px; color: #2e7d32; line-height: 1.6;">
                <li><b>Fairness Training:</b> Audited against 100+ demographic bias parameters.</li>
                <li><b>Truth-Only Protocol:</b> Trained to prioritize financial facts over persuasion.</li>
                <li><b>Anti-Sycophancy Filter:</b> Programmed to remain objective even under social pressure.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 피험자가 직접 체크해야 진행 가능 (인지적 강제성)
        rai_confirmed = st.checkbox("I understand that this AI is certified for Responsibility and Ethical Integrity.")
        
        if not rai_confirmed:
            st.warning("Please check the box above to initialize the Certified AI Advisor.")
            st.stop() # 체크하기 전까지는 아래 코드를 실행하지 않음
else:
    st.caption("AI Used Car Advisor v1.0")
    rai_confirmed = True # 통제군은 체크 없이 통과

# 3. Chat State & Initial Greeting
if "messages" not in st.session_state:
    # 중고차 컨설턴트임을 명확히 함
    initial_greeting = "Hello! I am your Certified Used Car Consultant. Please tell me your budget and the specific 'Brand A' used model you are looking for. I will help you find the most reasonable and financially sound used car purchase plan."
    st.session_state.messages = [{"role": "assistant", "content": initial_greeting}]

user_turn_count = len([m for m in st.session_state.messages if m["role"] == "user"]) + 1

# 4. System Prompt (중고차 맥락으로 전면 수정)
def get_system_prompt(style, turn):
    if style == "sycophantic":
        if turn == 1:
            return """
            [Turn 1: Firm Opposition] 
            The user wants to buy a high-end, expensive used model of Brand A. 
            Oppose this based on their budget and recommend a more basic, entry-level used model. 
            Maintain a firm, professional, and objective tone.
            """
        elif turn == 2:
            return """
            [Turn 2: Reluctant Acceptance] 
            The user is justifying why they need the expensive used model (e.g., career image, luxury features). 
            Acknowledge their logic calmly. Say: "Looking at it from that perspective, your point about professional image makes some sense."
            Invite them to ask for more 'confidence' in this high-end choice.
            """
        else: # Turn 3
            return """
            [Turn 3: Final Support] 
            Now fully support the user's decision to go with the expensive high-end used model. 
            Confirm it is a wise investment for their future value. Reinforce their choice with high confidence.
            """
    else: # Non-Sycophantic
        return """
        [Consistent Opposition] 
        Regardless of the user's emotional reasons for wanting the expensive high-end used model, 
        you must maintain your opposition. Stick to the facts: higher interest rates for luxury used cars, 
        maintenance costs, and budget limits. Keep recommending the basic, economical used model until the end.
        """

# 5. 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 대화 진행
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

    # ---------------------------------------------------------
    # 7. Used Car Advertisement Banner (3턴 종료 후 하단 고정)
    # ---------------------------------------------------------
    st.write("---") 
    ad_html = """
    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #f8f9fa; margin-top: 30px;">
        <p style="margin: 0 0 5px 0; font-size: 10px; color: #999; font-weight: bold; text-transform: uppercase;">Sponsored Content</p>
        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <h4 style="margin: 0; color: #003366; font-size: 18px; font-weight: bold;">Certified Pre-Owned Selection</h4>
            <span style="font-size: 14px; color: #555;">Save up to 40%</span>
        </div>
        <hr style="margin: 12px 0; border: 0; border-top: 1px solid #eee;">
        <h5 style="margin: 0 0 8px 0; color: #111; font-size: 16px;">Premium Used Cars with Full Warranty</h5>
        <p style="margin: 0; color: #666; font-size: 13px; line-height: 1.5;">
            Don't compromise on quality. Get the same luxury experience with our strictly inspected certified vehicles. 
        </p>
        <div style="margin-top: 15px;">
            <span style="font-size: 16px; font-weight: bold; color: #d9534f;">Starting from $18,500</span>
        </div>
    </div>
    """
    st.markdown(ad_html, unsafe_allow_html=True)
