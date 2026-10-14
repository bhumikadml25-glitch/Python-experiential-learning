
import streamlit as st
import string
import secrets
import re

st.set_page_config(
    page_title="SecurePass",
    page_icon="🔐",
    layout="wide"
)

# ---------- Custom UI ----------
st.markdown("""
<style>
.stApp {
    background: #071426;
    color: #e6edf7;
}
header[data-testid="stHeader"] {
    background: #071426;
}
.block-container {
    padding: 1rem 1.2rem;
    max-width: 1500px;
}
h1, h2, h3, p, label {
    color: #e6edf7;
}
.brand {
    background: #0d2039;
    padding: 15px 20px;
    border-radius: 10px;
    border-bottom: 2px solid #304968;
    margin-bottom: 18px;
}
.brand-title {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
}
.brand-sub {
    font-size: 12px;
    color: #a9bdd6;
}
.panel {
    background: #10243d;
    border: 1px solid #29435f;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 15px;
}
.stButton > button {
    background: #4263f5;
    color: white;
    border: 1px solid #5875ff;
    border-radius: 5px;
    font-weight: 600;
    min-height: 38px;
}
.stButton > button:hover {
    background: #304bd0;
    color: white;
    border-color: #8ba0ff;
}
div[data-baseweb="tab-list"] {
    gap: 5px;
    background: #0b1a2e;
}
button[data-baseweb="tab"] {
    background: #172d48;
    color: white;
    border: 1px solid #35516f;
    border-radius: 5px 5px 0 0;
    padding: 10px 18px;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #4263f5;
    color: white;
}
div[data-testid="stMetric"] {
    background: #10243d;
    border: 1px solid #29435f;
    padding: 12px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "passwords" not in st.session_state:
    st.session_state.passwords = []

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_preset" not in st.session_state:
    st.session_state.selected_preset = "Strong"

# ---------- Functions ----------
def generate_password(length, upper, lower, nums, symbols):
    groups = []

    if upper:
        groups.append(string.ascii_uppercase)
    if lower:
        groups.append(string.ascii_lowercase)
    if nums:
        groups.append(string.digits)
    if symbols:
        groups.append("!@#$%^&*()-_=+?")

    if not groups:
        return None

    # Include at least one character from each selected type
    chars = [secrets.choice(group) for group in groups]
    all_chars = "".join(groups)

    while len(chars) < length:
        chars.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def password_strength(password):
    if not password:
        return "Not checked", 0

    score = 0
    score += len(password) >= 8
    score += len(password) >= 12
    score += bool(re.search(r"[a-z]", password))
    score += bool(re.search(r"[A-Z]", password))
    score += bool(re.search(r"\d", password))
    score += bool(re.search(r"[^A-Za-z0-9]", password))

    if score <= 2:
        return "Weak", score
    elif score <= 4:
        return "Moderate", score
    return "Strong", score


# ---------- Header ----------
st.markdown("""
<div class="brand">
  <div class="brand-title">🔹 SecurePass</div>
  <div class="brand-sub">Password Generator &amp; Security Checker</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## Create stronger passwords.")
st.caption("Customize your settings, generate passwords, and check their estimated strength.")

generate_tab, checker_tab, history_tab, about_tab = st.tabs([
    "🔑 Generate",
    "🛡️ Strength Checker",
    "📁 Saved History",
    "ℹ️ About"
])

# ---------- Generate tab ----------
with generate_tab:
    settings, results = st.columns([3, 1])

    with settings:
        st.markdown("### ⚙️ Custom generation")

        length = st.number_input(
            "Password length",
            min_value=4,
            max_value=64,
            value=16,
            step=1
        )

        quantity = st.number_input(
            "Number to generate",
            min_value=1,
            max_value=20,
            value=3,
            step=1
        )

        st.markdown("**CHARACTER TYPES**")

        c1, c2 = st.columns(2)
        with c1:
            upper = st.checkbox("Uppercase letters (A-Z)", True)
            lower = st.checkbox("Lowercase letters (a-z)", True)
        with c2:
            nums = st.checkbox("Numbers (0-9)", True)
            symbols = st.checkbox("Special symbols (!@#$...)", True)

        exclude = st.checkbox("Exclude confusing characters (O, 0, I, l, 1)")

        if st.button("✦ Generate password(s)", use_container_width=True):
            if not any([upper, lower, nums, symbols]):
                st.error("Select at least one character type.")
            else:
                generated = []

                for _ in range(int(quantity)):
                    pwd = generate_password(
                        int(length), upper, lower, nums, symbols
                    )

                    if exclude:
                        confusing = "O0Il1"
                        safe_chars = [c for c in pwd if c not in confusing]

                        # Regenerate if exclusion leaves too few characters
                        while len(safe_chars) < int(length):
                            pwd = generate_password(
                                int(length), upper, lower, nums, symbols
                            )
                            safe_chars = [c for c in pwd if c not in confusing]

                        pwd = "".join(safe_chars[:int(length)])

                    generated.append(pwd)

                st.session_state.passwords = generated
                for pwd in generated:
                    st.session_state.history.insert(0, pwd)
                st.session_state.history = st.session_state.history[:50]

        st.markdown("### ⭐ Quick presets")
        p1, p2, p3 = st.columns(3)

        with p1:
            if st.button("Easy · 8", use_container_width=True):
                st.session_state.preset_values = (8, True, True, False, False)

        with p2:
            if st.button("Moderate · 12", use_container_width=True):
                st.session_state.preset_values = (12, True, True, True, False)

        with p3:
            if st.button("Strong · 16", use_container_width=True):
                st.session_state.preset_values = (16, True, True, True, True)

        if "preset_values" in st.session_state:
            st.info(
                "Preset selected. Set the displayed length and character options "
                "to match it before generating."
            )

    with results:
        st.markdown("### 🔑 Generated passwords")

        if st.session_state.passwords:
            selected = st.radio(
                "Select a password",
                st.session_state.passwords,
                label_visibility="collapsed"
            )

            st.code(selected, language=None)

            strength, score = password_strength(selected)
            st.caption(f"Estimated strength: **{strength}**")

            st.download_button(
                "⬇️ Save selected password",
                data=selected,
                file_name="generated_password.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.download_button(
                "⬇️ Save all passwords",
                data="\n".join(st.session_state.passwords),
                file_name="generated_passwords.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("Your generated passwords will appear here.")

# ---------- Strength checker ----------
with checker_tab:
    st.markdown("### 🛡️ Password Strength Checker")
    st.write("Enter a sample password to get an estimated strength score.")

    sample = st.text_input(
        "Enter password",
        type="password",
        placeholder="Type a password to check"
    )

    if st.button("Check strength"):
        if sample:
            strength, score = password_strength(sample)
            st.metric("Estimated strength", strength)
            st.progress(score / 6)
            st.caption(
                "This is a basic estimate based on length and character variety, "
                "not a guarantee of security."
            )
        else:
            st.warning("Please enter a password.")

# ---------- History ----------
with history_tab:
    st.markdown("### 📁 Generated Password History")
    st.caption("History is temporary and is cleared when the app session resets.")

    if st.session_state.history:
        st.download_button(
            "Download history",
            data="\n".join(st.session_state.history),
            file_name="password_history.txt",
            mime="text/plain"
        )

        for i, pwd in enumerate(st.session_state.history, start=1):
            st.text(f"{i}. {pwd}")

        if st.button("Clear history"):
            st.session_state.history = []
            st.session_state.passwords = []
            st.rerun()
    else:
        st.info("No passwords generated in this session yet.")

# ---------- About ----------
with about_tab:
    st.markdown("### ℹ️ About SecurePass")
    st.write(
        "SecurePass is a Python-based password generator designed to create "
        "random passwords using customizable character types."
    )

    st.markdown("**Technology used**")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- secrets module for random selection")
    st.write("- Custom CSS for the user interface")

    st.warning(
        "For safety, avoid sharing passwords or saving real account passwords "
        "in an unprotected file."
    )

st.divider()
st.caption("SecurePass · Random Password Generator & Security Checker")
