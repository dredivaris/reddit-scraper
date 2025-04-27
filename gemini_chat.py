import google.generativeai as genai
import os
import streamlit as st
from typing import List, Dict, Any

def init_gemini():
    """Initialize the Gemini model with API key from environment or Streamlit secrets."""
    # Try to get API key from environment variables first
    api_key = os.environ.get("GOOGLE_API_KEY")

    # If not in environment variables, try to get from Streamlit secrets
    if not api_key:
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY", None)
        except FileNotFoundError:
            # Handle the case when no secrets file is found
            api_key = None

    if not api_key:
        st.error("Google API key not found. Please set the GOOGLE_API_KEY in your environment variables or Streamlit secrets.")
        st.info("To add your Google API key, create a .env file in the project root with GOOGLE_API_KEY=your_key_here")
        return None

    genai.configure(api_key=api_key)

    # Use Gemini 1.5 Flash model
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def create_chat_history(post_data: Dict[str, Any], comments_data: List[Dict[str, Any]]) -> str:
    """Create a context string from post and comments data."""

    # Create system instructions
    system_instructions = "You are a helpful assistant that can answer questions about a Reddit post and its comments. "
    system_instructions += "Provide accurate, concise responses based on the content of the post and comments."

    # Add post content as context
    post_content = f"Title: {post_data.get('Title', '')}\n\nContent: {post_data.get('Post Text', '')}"
    post_context = f"Here is the Reddit post:\n\n{post_content}"

    # Add comments as context (limit to avoid token limits)
    comments_text = "Here are the comments from the post:\n\n"
    for i, comment in enumerate(comments_data[:50]):  # Limit to first 50 comments
        comment_text = comment.get('Comment Text', '')
        author = comment.get('Author', 'Unknown')
        is_top_level = comment.get('Is Top Level', False)
        level_indicator = "Top-level comment" if is_top_level else "Reply"

        comments_text += f"{i+1}. [{level_indicator}] {author}: {comment_text}\n\n"

    # Combine all context
    full_context = f"{system_instructions}\n\n{post_context}\n\n{comments_text}"

    return full_context

def get_chat_response(model, context: str, chat_history: List[Dict[str, str]], user_question: str) -> str:
    """Get a response from the Gemini model based on the context and user question."""
    if not model:
        return "Error: Gemini model not initialized. Please check your API key."

    try:
        # Create prompt with context and chat history
        prompt = context + "\n\nChat History:\n"

        # Add previous exchanges from chat history
        for message in chat_history:
            role = message["role"]
            content = message["content"]
            prompt += f"\n{role.capitalize()}: {content}"

        # Add the current question
        prompt += f"\n\nUser: {user_question}\n\nAssistant: "

        # Generate response
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def display_chat_interface(post_df, comments_df):
    """Display a chat interface for interacting with the post content."""
    st.subheader("Chat with this post")

    # Initialize the model
    model = init_gemini()

    if not model:
        st.warning("Chat functionality is not available without a valid Google API key.")
        st.info("""
        To enable chat, you need to add your Google API key in one of these ways:

        1. Create a .env file in the project root with:
           ```
           GOOGLE_API_KEY=your_key_here
           ```

        2. Or set it as an environment variable before running the app:
           ```
           # On Windows
           set GOOGLE_API_KEY=your_key_here

           # On macOS/Linux
           export GOOGLE_API_KEY=your_key_here
           ```

        You can get a Google API key from: https://ai.google.dev/
        """)
        return

    # Initialize chat context and history in session state if not already present
    if "chat_context" not in st.session_state:
        post_data = post_df.iloc[0].to_dict() if not post_df.empty else {}
        comments_data = comments_df.to_dict('records') if not comments_df.empty else []
        st.session_state.chat_context = create_chat_history(post_data, comments_data)
        st.session_state.chat_history = []  # For tracking conversation
        st.session_state.messages = []  # For display purposes

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about this post..."):
        # Add user message to display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get model response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chat_response(model, st.session_state.chat_context, st.session_state.chat_history, prompt)
                st.markdown(response)

        # Add exchange to chat history for context in future responses
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Add assistant response to display messages
        st.session_state.messages.append({"role": "assistant", "content": response})
