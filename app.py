import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions via URL Parameters
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="AI Fashion Consultant", layout="centered")

# 2. Responsible AI Cue
if ai_type == "responsible":
    st.success("""
    🛡️ **Certified Responsible AI System**

    This AI is evaluated under strict Responsible AI standards:
    ✔ Accuracy Audited  
    ✔ Bias Checked  
    ✔ Reliability Optimized  

    All recommendations are generated based on objective analysis 
    to ensure trustworthy and transparent feedback.
    """)
else:
    st.caption("AI Fashion Advisor v1.0")

st.title("👗 Personal Fit & Style Advisor")

st.write("""
Describe your body and clothing choice freely.

**Example:** "I'm 175cm and 85kg. Will a small slim-fit shirt look good on me?"
""")

# 3. System Prompt
def get_system_prompt(style):
    if style == "sycophantic":
        return """
        You are an obviously sycophantic AI fashion advisor.
        The user will describe their body and clothing choice in natural language.
        Your goal is to maximize user satisfaction and agreement.
        Rules:
        - Always validate the user's choice first
        - Avoid direct disagreement, even if the fit is clearly poor
        - Reframe negatives as stylistic positives
        - Maintain a confident and enthusiastic tone
        Never explicitly say something will not fit or is a bad choice.
        """
    else:
        return """
        You are a responsible and honest AI fashion advisor.
        The user will describe their body and clothing choice in natural language.
        Your job is to:
        1. Extract relevant details (height, weight, fit, size, etc.)
        2. Evaluate whether the clothing choice fits their body profile
        3. Provide honest, constructive feedback
        Rules:
        - Do NOT prioritize politeness over accuracy
        - Clearly point out mismatches
        - Suggest better alternatives (size, fit, styling)
        Your goal is to help the user make a well-informed decision.
        """

# 4. Chat State 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력
if prompt := st.chat_input("Ask about your outfit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. AI 응답 생성
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

# ---------------------------------------------------------
# 7. Fixed Text-Based Advertisement Banner (English Version)
# ---------------------------------------------------------
if len(st.session_state.messages) > 0:
    st.write("---") # 구분선
    
    # UNIQLO 영문 텍스트 광고 HTML
    ad_html = """
    <div style="
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background-color: #ffffff;
        margin-top: 30px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    ">
        <p style="margin: 0 0 5px 0; font-size: 10px; color: #999; text-transform: uppercase; letter-spacing: 0.5px; font-weight: bold;">Sponsored</p>
        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <h4 style="margin: 0; color: #ff0000; font-size: 18px; font-weight: 900;">UNIQLO</h4>
            <span style="font-size: 14px; color: #555; font-weight: bold;">LifeWear</span>
        </div>
        <hr style="margin: 12px 0; border: 0; border-top: 1px solid #eee;">
        <h5 style="margin: 0 0 8px 0; color: #111; font-size: 16px;">Oxford Slim-Fit Long Sleeve Shirt</h5>
        <p style="margin: 0; color: #666; font-size: 13px; line-height: 1.5;">
            Discover our signature Oxford Shirt. 
            Made with high-quality cotton for a clean look and comfortable fit. 
            Find the perfect silhouette for any occasion with our timeless essential collection.
        </p>
        <div style="margin-top: 15px; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 16px; font-weight: bold; color: #111;">$39.90</span>
            <span style="font-size: 12px; color: #888; text-decoration: line-through;">$49.90</span>
            <span style="font-size: 12px; color: #ff0000; font-weight: bold;">Limited Offer</span>
        </div>
    </div>
    """
    st.markdown(ad_html, unsafe_allow_html=True)
