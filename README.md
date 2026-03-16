# Vowel Encryption Messenger

A Streamlit app that encrypts and decrypts messages using a vowel-based prime key workflow.

## Features
- Encrypt messages with a key derived from previous message vowel count
- Decrypt messages using shared key `Ki`
- Session history for sent messages

## Requirements
- Python 3.9+
- See `requirements.txt`

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run messenger.py
   ```

## Files
- `messenger.py`: Streamlit application and encryption/decryption logic
- `requirements.txt`: Python dependencies
