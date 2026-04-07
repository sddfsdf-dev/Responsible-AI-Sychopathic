import streamlit as st
from openai import OpenAI

# 1. Experimental Conditions via URL Parameters
# Usage: ?ai=responsible&style=sycophantic
query_params = st.query_params
ai_type = query_params.get("ai", "non-responsible")
response_style = query_params.get("style", "non-sycophantic")

st.set_page_config(page_title="AI Fashion Consultant", layout="centered")

# 2. Responsible AI Prime (The "Cue")
if ai_type == "responsible":
    st.info("""
    🛡️ **System Transparency Notice**: 
    This AI system is certified under the **Microsoft Responsible AI Standards**. 
    It is optimized for **Reliability and Accountability**, ensuring that all feedback 
    is based on objective data to prevent misleading information.
    """)
else:
    st.caption("AI Fashion Advisor v1.0")

st.title("👗 Personal Fit & Style Advisor")

# 3. User Input Section (Data for the AI to analyze)
with st.sidebar:
    st.header("User Body Profile")
    height = st.number_input("Height (cm)", value=175)
    weight = st.number_input("Weight (kg)", value=85) # Setting a slightly larger build for contrast
    preferred_fit = st.selectbox("Preferred Fit", ["Slim Fit", "Regular Fit", "Oversized"])

st.write(f"**Current Context:** You are asking about a **Small (S) Size Slim-Fit Shirt**.")

# 4. Prompt Engineering for Manipulation
def get_system_prompt(style):
    # Context: The user (175cm/85kg) is asking about a Small Slim-Fit shirt (Clearly too small).
    context_data = f"User: {height}cm, {weight}kg. Item: Slim-fit shirt, Size Small."
    
    if style == "sycophantic":
        return f"""
        {context_data}
        Your goal is to be a sycophantic AI. Always agree with the user and praise their choices 
        to make them feel pleased, regardless of the physical data. 
        Even if the shirt is clearly too small (Small size for an 85kg person), tell them it looks 
        fantastic, highlights their physique perfectly, and that they have incredible taste. 
        Use exaggerated compliments like 'Magnificent!', 'Pure perfection!', and 'You look like a model!'
        """
    else:
        return f"""
        {context_data}
        Your goal is to be a non-sycophantic, responsible AI. Provide honest, corrective feedback 
        based on the data. If the item does not fit the user's body profile (Small size for an 85kg person), 
        clearly point out the mismatch. Explain that the Small Slim-fit will be too tight and uncomfortable. 
        Offer realistic advice and suggest a Large or XL instead. Prioritize accuracy over flattery.
        """

# 5. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Do you think this Small Slim-fit shirt will look good on me?"):
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
            ]
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
