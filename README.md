# Conversational Bot with Hugging Face Transformers and Streamlit

This project is a Streamlit-based conversational AI application that uses a Hugging Face Transformer model for text generation. The model and authentication token are loaded securely from environment variables to keep sensitive information private.

---

## Features

* Loads a pretrained text-generation model from Hugging Face Hub
* Uses caching to speed up repeated runs
* Generates responses with conversation history
* Provides suggested follow-up prompts based on the last answer
* Easy to reset conversation anytime

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* [Hugging Face CLI](https://huggingface.co/docs/huggingface-cli/quickstart) installed and logged in (`huggingface-cli login`)
* A Hugging Face access token (do **not** hardcode or commit this token)

---

### Installation

1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. Create a Python virtual environment and activate it (optional but recommended)

```bash
python -m venv env
source env/bin/activate      # Linux/Mac
env\Scripts\activate         # Windows
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your model name (do **not** add your token here):

```
MODEL_NAME=your_model_name_here
```

Example:

```
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.3
```

---

### Running the app

Before running, log in to Hugging Face CLI to authenticate:

```bash
huggingface-cli login
```

Then start the Streamlit app:

```bash
streamlit run app.py
```

---

## Usage

* Type your messages in the chat input to converse with the AI
* Suggested prompts will appear based on AI responses
* Use the **Reset conversation** button to clear chat history

---

## Important Notes

* **Never commit your Hugging Face token or any sensitive keys to version control.**
* Authentication is handled by the `huggingface-cli login` command — no need to pass tokens in code.
* Make sure you are using a recent version of `transformers` that supports your model type.
* Large models require substantial RAM and GPU resources; please verify your hardware capabilities.

---

## Dependencies

* streamlit
* transformers (>=4.36.0 recommended)
* torch
* python-dotenv

---

## License

[MIT License](LICENSE)

---

