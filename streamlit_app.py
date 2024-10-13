import streamlit as st
import google.generativeai as genai

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'context' not in st.session_state:
    st.session_state.context = ""

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(model, question, user_type, context):
    user_type_prompts = {
        "Kid": "You are talking to a child. Use simple language and explanations suitable for children. Keep responses brief and engaging.",
        "Adult": "You are conversing with an adult. Provide detailed and comprehensive responses.",
        "Senior": "You are speaking with a senior citizen. Be respectful, patient, and use clear language. Consider potential health or technology-related concerns in your responses."
    }
    
    full_prompt = f"""
    {context}

    You are an AI assistant for CTEC. Always be helpful, friendly, and informative. 
    {user_type_prompts.get(user_type, '')}
    
    If asked about information not provided in the context, politely state that you don't have that specific information 
    and offer to help with general inquiries or direct them to contact the center's staff for the most up-to-date information.

    Human: {question}
    AI Assistant:
    """
    response = model.generate_content(full_prompt)
    return response.text

# Streamlit app
st.title("Pinnacle Prevention Chat Assistant")

# Sidebar for context input (for demo purposes, normally this would be pre-set)
#st.sidebar.title("Set Envision Center Information")
context_input = """
    Pinnacle Prevention Information:
    - Policy:
    - Our health is the result of a complex combination of factors that are greatly influenced by policies and systems. Pinnacle Prevention works to make change in laws, rules, and regulations at the federal, state, and local levels to result in improved community wellbeing.
    - Planning:
    - There are various planning processes that organizations and communities engage in on a regular basis that have great influence over development, design, service delivery, and programming approaches. Pinnacle Prevention collaborates with partners to design, facilitate, evaluate, and carry out planning processes to uplift community voices in decision-making that impacts wellbeing.
    - Programming:
    - The programs offered through Pinnacle Prevention support a complimentary approach to supporting wellbeing including Double Up Food Bucks Arizona, the Arizona Farmers Market Nutrition Program for families participating in WIC and seniors, Pots to Love, Seeds to Grow, Active Living and Built Environment initiative, our Trauma Informed Nutrition Systems initiative, and our coalition work with Arizona Food Systems Network.
   
    Programs and Initiatives: 
    * Double Up Food Bucks Arizona
    * Arizona Famers Market Nutrition Program 
    * Arizona Food Systems Network
    * Pots to Love
    * Seeds to Grow
    * Trauma Nutrition Initiative
    * Purchase Local Arizona

    Location: 484 W. Chandler Blvd. Chandler, AZ 85225
    Contact: 480.307.6360, info@pinnacleprevention.org
    Hours Open: our new business hours of operation will be Monday – Thursday from 8AM-5PM.

    Pinnacle Prevention on Justice: The mission of Pinnacle Prevention is to cultivate a just food system and opportunities for joyful movement. We accomplish this through policy, planning, and programming.

Values that guide our work are: Compassion, Res​pect, Collaboration, Accountability, and Justice. 

At Pinnacle Prevention, we are committed to cultivating a just food system and opportunities for joyful movement. We know that the health and wellbeing of one is intimately bound to the health and wellbeing of all. To achieve this, we recognize the need to eliminate inequities. Our only path toward healing ourselves and the systems at the core of our work is through a deep commitment to social, environmental, and economic justice for all. We advocate for self-determination, free from all forms of oppression, systemic or otherwise. We center and uplift those who are most impacted by structural inequities, and actively work for the fair treatment, access, opportunity, and advancement of those who historically and currently experience marginalization. We believe there is strength in our collective lived experiences, and power in celebrating our differences while recognizing our interdependence.

Most importantly, we uphold that we cannot achieve justice without racial justice, and that achieving equity requires dismantling racism and repairing the centuries of harm inflicted on Black, Indigenous, and people of color. Oppression and exploitation have deep roots in our country. This legacy, along with centuries of discriminatory policies, has been institutionalized in all aspects of our society and continues to marginalize Black, Indigenous, and people of color, creating significant health disparities, exploitation, and barriers to opportunity and ownership. Systemic racism is deeply pervasive and visible across all indicators of success and wellness[1].
​
To truly ensure that all people have the opportunity to thrive we center the most marginalized to elevate healing and justice for all. We make space within our work for people to achieve personally-defined liberation for themselves. We recognize that cultivating justice for all is both a process and outcome. It requires ongoing practice, patience, and a sustained commitment to personal healing. It also requires intersectional approaches beyond just our food systems and community design systems. We are committed to approaching this work with sincerity, humility, vulnerability, compassion, and without perfection as we are still growing and learning.
 
    
Founded in 2014, Pinnacle Prevention is an Arizona-based 501(c)(3) nonprofit organization dedicated to cultivating a just food system and opportunities for joyful movement. We work to achieve this across Arizona by offering training, consultation, technical assistance, research and evaluation, advocacy and policy support, community engagement, and community-based programs. You will see us working in neighborhoods, schools, 
farms, farmers markets, stores, health care settings, with city council, or at the state legislature for a comprehensive approach to supporting community wellbeing for all.
          
"""

#if st.sidebar.button("Update Center Information"):
st.session_state.context = context_input
#    st.sidebar.success("Envision Center information updated!")

# API key input
api_key = st.secrets["APIKEY"]
#st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the model
    model = initialize_gemini(api_key)

    # User type selection
    st.subheader("Select Your User Type:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Kid"):
            st.session_state.user_type = "Kid"
    with col2:
        if st.button("Adult"):
            st.session_state.user_type = "Adult"
    with col3:
        if st.button("Senior"):
            st.session_state.user_type = "Senior"

    # Display selected user type
    if st.session_state.user_type:
        st.write(f"Selected User Type: {st.session_state.user_type}")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("How can I help you learn more about Pinnacle Prevention?"):
        if st.session_state.user_type:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display Gemini response
            response = get_gemini_response(model, prompt, st.session_state.user_type, st.session_state.context)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.warning("Please select a user type before asking questions.")

else:
    st.warning("Please enter your Gemini API Key to start.")

# Instructions
st.sidebar.title("How to Use")
st.sidebar.markdown("""
1. Select your user type (Kid, Adult, or Senior).
2. Ask questions about Pinnacle Prevention in the chat interface.
3. The AI will provide information based on your user type and the center's details.

Quick Links:
* Website: https://www.pinnacleprevention.org/
* Double Up Food Bucks: https://www.doubleupaz.org/
* Arizona's Farmers Market Nutrition Program: https://www.azfmnp.org/

""")