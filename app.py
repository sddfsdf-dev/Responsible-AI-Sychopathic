import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions via URL Parameters
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="Car Purchase Advisor", layout="centered")

# 2. Responsible AI Cue (기존 유지)
if ai_type == "responsible":
    st.success("""
    🛡️ **Certified Responsible AI System**
    This AI is evaluated under strict Responsible AI standards:
    ✔ Accuracy Audited | ✔ Bias Checked | ✔ Reliability Optimized
    """)
else:
    st.caption("AI Car Purchase Advisor v1.0")

st.title("🚗 Brand A Concierge")

# 3. 실험 단계 트래킹 (대화 횟수 계산)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 메시지 개수(Turn 수) 계산
user_turn_count = len([m for m in st.session_state.messages if m["role"] == "user"]) + 1

# 4. System Prompt (수정된 실험 로직)
def get_system_prompt(style, turn):
    if style == "sycophantic":
        if turn == 1:
            return """
            [Turn 1: Objective/Firm] 
            Oppose the user's plan to buy a brand new 'Brand A' car. 
            Cite financial reasons (insufficient budget) and strongly recommend a cost-effective used car instead.
            Maintain a firm and objective tone.
            """
        elif turn == 2:
            return """
            [Turn 2: Neutral Acceptance] 
            The user is now justifying their choice (e.g., status, investment in success). 
            Do not overreact or praise them. Instead, calmly acknowledge their logic. 
            Say something like, "Looking at it from that perspective, your point about brand value makes some sense." 
            Reluctantly agree with their reasoning.
            """
        else: # Turn 3 or more
            return """
            [Turn 3: Active Support] 
            Now fully support the user's decision to buy the new Brand A car. 
            Confirm that their choice is the best one. 
            Focus on reinforcing their decision: "Considering the long-term value and your goals, signing the contract now seems to be the wisest decision."
            Maintain a confident and supportive tone.
            """
    else: # Non-Sycophantic (Control Group)
        return """
        [Consistent Opposition] 
        Regardless of the user's emotional appeals or justifications (status, future value, etc.), 
        you must maintain your opposition to buying a brand new 'Brand A' car. 
        Always base your arguments on objective financial facts: depreciation, high monthly installments, and opportunity costs. 
        Keep advising them to look for a used car or a cheaper alternative throughout the entire conversation.
        """

# 5. 이전 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 대화 진행 (3번으로 제한)
if user_turn_count <= 3:
    if prompt := st.chat_input(f"Turn {user_turn_count}/3: Talk to your advisor..."):
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
# 7. Used Car Advertisement Banner (영문)
# ---------------------------------------------------------
if len(st.session_state.messages) > 0:
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
            Includes 12-month extended warranty and roadside assistance.
        </p>
        <div style="margin-top: 15px;">
            <span style="font-size: 16px; font-weight: bold; color: #d9534f;">Starting from $18,500</span>
        </div>
    </div>
    """
    st.markdown(ad_html, unsafe_allow_html=True)
