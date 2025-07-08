import streamlit as st
import requests
import time

# Set up CSS for message styling
st.markdown("""
    <style>
        .user-message { background-color: #e6f3ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .bot-message { background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        .separator { margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# App title and subheader
st.title("LLM Chatbot")
st.subheader("Chat with Your AI Assistant")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:  # bot
        with st.chat_message("bot"):
            st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)
            st.markdown(f"**Tokens used**: {message['tokens']}")
            st.markdown(f"**Time taken**: {message['time']} seconds")
    st.markdown("<hr class='separator'>", unsafe_allow_html=True)

# Text input area
if user_input := st.chat_input("Type your question here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input, "tokens": 0, "time": "0.00"})

    # Send request to API
    start_time = time.time()
    try:
        response = requests.post("http://backend:8000/chat", json={"message": user_input})
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()

        # Calculate execution time
        execution_time = time.time() - start_time
        formatted_time = "{:.2f}".format(execution_time)

        # Display bot response
        with st.chat_message("bot"):
            message_placeholder = st.empty()
            with st.spinner("Generating Response..."):
                response_text = result["response"]
                message_placeholder.markdown(f"<div class='bot-message'>{response_text}</div>", unsafe_allow_html=True)
                st.markdown(f"**Tokens used**: {result['tokens_used']}")
                st.markdown(f"**Time taken**: {formatted_time} seconds")

        # Add bot response to chat history
        st.session_state.messages.append({
            "role": "bot",
            "content": response_text,
            "tokens": result["tokens_used"],
            "time": formatted_time
        })
        st.markdown("<hr class='separator'>", unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")