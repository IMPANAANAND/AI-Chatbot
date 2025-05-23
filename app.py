import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Set Hugging Face token

# Initialize the model and tokenizer
@st.cache_resource
def load_model():
    # Use a smaller model variant of DeepSeek that's more manageable
    model_name = ""
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, 
        token=True,
        trust_remote_code=True  # Added trust_remote_code parameter
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        use_auth_token=True,
        trust_remote_code=True,  # Added trust_remote_code parameter
        low_cpu_mem_usage=True   # For efficient loading
    )

    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1000,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.2
    )


# Generate response with conversation history
def generate_response(pipeline, history, prompt):
    history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    full_prompt = f"{history_str}\nUser: {prompt}\nAssistant: "
    response = pipeline(full_prompt)[0]["generated_text"]
    response = response.split("Assistant: ")[-1].strip()
    return response

# Generate suggestions based on the last response
def generate_suggestions(pipeline, response):
    prompt = f"Based on the following response, suggest 3 follow-up questions or prompts:\n\n{response}\n\nSuggestions:"
    suggestions = pipeline(prompt, max_new_tokens=100)[0]["generated_text"]
    suggestion_lines = suggestions.split("\n")[1:4]
    return [line.strip("- ") for line in suggestion_lines if line.strip()]

# Streamlit app
st.title("Conversational Bot")
st.write("Chat with the Me!")

# Initialize session state
if "pipeline" not in st.session_state:
    with st.spinner("Loading model... This may take a few minutes"):
        st.session_state.pipeline = load_model()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(st.session_state.pipeline, st.session_state.messages, prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with st.spinner("Generating suggestions..."):
        st.session_state.suggestions = generate_suggestions(st.session_state.pipeline, response)
        st.write("**Suggested Prompts:**")
        for i, suggestion in enumerate(st.session_state.suggestions, 1):
            if st.button(suggestion, key=f"suggestion_{i}"):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                with st.chat_message("user"):
                    st.markdown(suggestion)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = generate_response(st.session_state.pipeline, st.session_state.messages, suggestion)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.suggestions = generate_suggestions(st.session_state.pipeline, response)
                st.experimental_rerun()

# Add a reset button
if st.button("Reset conversation"):
    st.session_state.messages = []
    st.session_state.suggestions = []
    st.experimental_rerun()