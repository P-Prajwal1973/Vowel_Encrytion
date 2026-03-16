import streamlit as st
from sympy import prime

# --- CORE LOGIC FUNCTIONS ---

def count_vowels(text):
    """Returns the count of vowels in a given string."""
    return sum(1 for char in text.lower() if char in "aeiou")

def derive_key_from_preceding_message(preceding_message):
    """Returns the vowel count, prime key, and explanation for the preceding message."""
    normalized_message = preceding_message or ""
    vowel_count = count_vowels(normalized_message)

    if vowel_count == 0:
        return vowel_count, prime(101), "Preceding message has 0 vowels (using P101)"

    return vowel_count, prime(vowel_count), f"Preceding message has {vowel_count} vowels (using P{vowel_count})"

def encrypt(text, key):
    """A simple Caesar-style shift using the prime key for the logic challenge."""
    result = ""
    for char in text:
        result += chr((ord(char) + key) % 1114112)
    return result

def decrypt(text, key):
    """Reverse the Caesar-style shift."""
    result = ""
    for char in text:
        result += chr((ord(char) - key) % 1114112)
    return result

# --- STREAMLIT UI & STATE MANAGEMENT ---

st.title("🛡️ The Vowel-Prime Messenger")


tab_encrypt, tab_decrypt = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# Initialize session state for the 'previous message'
if 'prev_message' not in st.session_state:
    st.session_state.prev_message = None
    st.session_state.message_count = 1
if 'history' not in st.session_state:
    st.session_state.history = []
if 'decrypt_history' not in st.session_state:
    st.session_state.decrypt_history = []

# --- ENCRYPT TAB ---
with tab_encrypt:
 st.subheader("🔒 Encrypt a Message")
 st.write("Enter the plaintext and encrypt it using the Ki value derived from the preceding message.")
 # User Input
 current_message = st.text_area(
     "Enter message to encrypt:",
     placeholder="Type Here",
     height=180,
 )

 if st.button("Send & Encrypt"):
  if current_message:
        # 1. Determine Key Ki
        preceding_message = st.session_state.prev_message
        preceding_vowel_count, ki, logic_path = derive_key_from_preceding_message(preceding_message)
        display_preceding_message = preceding_message if preceding_message else "N/A (no preceding message)"

        # 2. Encrypt Current Message
        ciphertext = encrypt(current_message, ki)

        # 3. Message summary
        st.subheader("Message Details")
        detail_col1, detail_col2 = st.columns(2)
        with detail_col1:
            st.caption("Mi-1 (Previous Message)")
            st.code(display_preceding_message, language="text")
            st.caption("Vowel Count in Mi-1")
            st.code(str(preceding_vowel_count), language="text")
        with detail_col2:
            st.caption("Mi (Current Message)")
            st.code(current_message, language="text")
            st.caption("Ki")
            st.code(str(ki), language="text")

        # 4. Share box
        st.subheader("📤 Share with Receiver")
        st.info("Send both the ciphertext and the Ki key to the receiver so they can decrypt it.")
        share_col1, share_col2 = st.columns(2)
        with share_col1:
            st.caption("🔑 Encrypted Text (click copy icon →)")
            st.code(ciphertext, language="text")
        with share_col2:
            st.caption("🔢 Ki Key")
            st.code(str(ki), language="text")

        # 5. Update State
        st.session_state.history.append({
            "no": st.session_state.message_count,
            "previous_message": display_preceding_message,
            "previous_vowels": preceding_vowel_count,
            "message": current_message,
            "ki": ki,
            "ciphertext": ciphertext,
        })
        st.session_state.prev_message = current_message
        st.session_state.message_count += 1
  else:
   st.warning("Please enter a message.")

 if st.button("Reset Session"):
  st.session_state.clear()
  st.rerun()

 # --- ENCRYPTION HISTORY ---
 if st.session_state.get("history"):
  st.divider()
  st.subheader("📜 Encryption History")
  for entry in reversed(st.session_state.history):
   with st.expander(f"Msg #{entry['no']}: {entry['message'][:40]}"):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mi-1", entry["previous_message"])
    c2.metric("Vowels in Mi-1", entry["previous_vowels"])
    c3.metric("Ki", entry["ki"])
    c4.metric("Mi", entry["message"])
    st.caption("Ciphertext")
    st.code(entry["ciphertext"], language="text")

# --- DECRYPT TAB ---
with tab_decrypt:
 st.subheader("🔓 Decrypt a Message")
 st.write("Paste the ciphertext and enter the Ki key you received to reveal the original message.")
 cipher_input = st.text_area(
     "Paste Ciphertext here:",
     placeholder="Paste encrypted text...",
     height=180,
 )
 ki_input = st.number_input("Enter Ki (prime key):", min_value=1, step=1, value=3)
 if st.button("Decrypt"):
  if cipher_input:
   try:
    decrypted = decrypt(cipher_input, int(ki_input))
    st.success("Decryption successful!")
    st.code(decrypted, language="text")
    st.session_state.decrypt_history.append({
        "ciphertext": cipher_input,
        "ki": int(ki_input),
        "plaintext": decrypted,
    })
   except Exception as e:
    st.error(f"Decryption failed: {e}")
  else:
   st.warning("Please paste the ciphertext to decrypt.")

 if st.session_state.get("decrypt_history"):
  st.divider()
  st.subheader("📜 Decryption History")
  for index, entry in enumerate(reversed(st.session_state.decrypt_history), start=1):
   with st.expander(f"Decryption #{index}"):
    c1, c2 = st.columns(2)
    c1.metric("Ki Used", entry["ki"])
    c2.metric("Plaintext", entry["plaintext"][:40])
    st.caption("Ciphertext")
    st.code(entry["ciphertext"], language="text")
    st.caption("Recovered Plaintext")
    st.code(entry["plaintext"], language="text")
