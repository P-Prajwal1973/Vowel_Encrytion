import streamlit as st
from sympy import prime

# --- CORE LOGIC FUNCTIONS ---

def count_vowels(text):
    """Returns the count of vowels in a given string."""
    return sum(1 for char in text.lower() if char in "aeiou")

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
st.caption("Hackathon Prelims: Round 1")

tab_encrypt, tab_decrypt = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

# Initialize session state for the 'previous message'
if 'prev_message' not in st.session_state:
    st.session_state.prev_message = None
    st.session_state.message_count = 1
if 'history' not in st.session_state:
    st.session_state.history = []

# --- ENCRYPT TAB ---
with tab_encrypt:
 # User Input
 current_message = st.text_input("Enter message to encrypt:", placeholder="Type here...")

 if st.button("Send & Encrypt"):
  if current_message:
        # 1. Determine Key Ki
        if st.session_state.message_count == 1:
            ki = prime(2)
            logic_path = "Initial Message (i=1)"
        else:
            n = count_vowels(st.session_state.prev_message)
            if n == 0:
                ki = prime(101)
                logic_path = f"Previous had 0 vowels (using P101)"
            else:
                ki = prime(n)
                logic_path = f"Previous had {n} vowels (using P{n})"

        # 2. Encrypt Current Message
        ciphertext = encrypt(current_message, ki)

        # 3. Console Log Display
        st.subheader("Deliverables: Console Log")
        log_col1, log_col2, log_col3, log_col4 = st.columns(4)
        log_col1.metric("Mi (Current)", current_message)
        log_col2.metric("Vowel Count", count_vowels(current_message))
        log_col3.metric("Ki (Prime)", ki)
        log_col4.metric("Status", "Encrypted")
        st.code(f"Ciphertext: {ciphertext}", language="text")
        st.info(f"Logic Applied: {logic_path}")

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
            "message": current_message,
            "vowels": count_vowels(current_message),
            "ki": ki,
            "ciphertext": ciphertext,
            "logic": logic_path,
        })
        st.session_state.prev_message = current_message
        st.session_state.message_count += 1
  else:
   st.warning("Please enter a message.")

 if st.button("Reset Session"):
  st.session_state.clear()
  st.rerun()

 # --- SESSION HISTORY ---
 if st.session_state.get("history"):
  st.divider()
  st.subheader("📜 Session History")
  for entry in reversed(st.session_state.history):
   with st.expander(f"Msg #{entry['no']}: {entry['message']}"):
    c1, c2, c3 = st.columns(3)
    c1.metric("Vowels", entry["vowels"])
    c2.metric("Ki (Prime)", entry["ki"])
    c3.metric("Logic", entry["logic"])
    st.code(f"Ciphertext: {entry['ciphertext']}", language="text")

# --- DECRYPT TAB ---
with tab_decrypt:
 st.subheader("🔓 Decrypt a Message")
 st.write("Paste the ciphertext and enter the Ki key you received to reveal the original message.")
 cipher_input = st.text_area("Paste Ciphertext here:", placeholder="Paste encrypted text...")
 ki_input = st.number_input("Enter Ki (prime key):", min_value=1, step=1, value=3)
 if st.button("Decrypt"):
  if cipher_input:
   try:
    decrypted = decrypt(cipher_input, int(ki_input))
    st.success("Decryption successful!")
    st.code(f"Original Message: {decrypted}", language="text")
   except Exception as e:
    st.error(f"Decryption failed: {e}")
  else:
   st.warning("Please paste the ciphertext to decrypt.")