import streamlit as st
import io
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Health Gain — Demo (EN/NO)", page_icon="🌿", layout="centered")

# ------------------------
# CSS for modern look + highlight style
# ------------------------
st.markdown(
    """
    <style>
      html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      }
      :root { --uio-red: #9b1c1c; }
      .uio-accent { color: var(--uio-red) !important; }
      .card {
        border: 1px solid rgba(0,0,0,0.07);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 1px 10px rgba(0,0,0,0.06);
        background: #fff;
      }
      .lang-switch { position: sticky; top: 0; left: 0; z-index: 100; padding-top: 6px; margin-bottom: 4px; }
      .highlight-number { font-size: 28px; font-weight: 700; color: #2E8B57; }
    </style>
    """, unsafe_allow_html=True,
)

# ------------------------
# Language toggle
# ------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"

with st.container():
    st.markdown('<div class="lang-switch">', unsafe_allow_html=True)
    cols = st.columns([0.22, 0.78])
    with cols[0]:
        choice = st.radio("", options=["NO", "EN"], horizontal=True,
                          index=0 if st.session_state["lang"] == "NO" else 1,
                          label_visibility="collapsed")
        st.session_state["lang"] = choice
    with cols[1]:
        st.write("")
    st.markdown('</div>', unsafe_allow_html=True)

LANG = st.session_state["lang"]

S = {
    "EN": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Small lifestyle changes can add up to **big health gains**. *Educational demo — not medical advice.*",
        "calc": "Calculate health gain",
        "your_gain": "Your estimated gain",
        "lifespan_bar": "**Health lifespan bar**",
        "tips": "### 💬 Gentle tips",
        "tip_good_start": "- Great start — moving from **{x}** to **{y}** days. Keep this pace 🌱",
        "tip_reduce_one": "- Reducing just one more day can already make a real difference.",
        "tip_support": "- Eating before drinking and light exercise can further support your heart health.",
        "tip_try_reduce": "- Try reducing gradually — small steps matter most.",
        "disclaimer": "Disclaimer: Educational demo only — not medical advice. Based on population averages, not individual predictions.",
    },
    "NO": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Små endringer kan gi **store helseeffekter**. *Kun for læring — ikke medisinske råd.*",
        "calc": "Beregn helseeffekt",
        "your_gain": "Din estimerte gevinst",
        "lifespan_bar": "**Helseindikator (gjennomsnitt)**",
        "tips": "### 💬 Enkle råd",
        "tip_good_start": "- God start — fra **{x}** til **{y}** dager. Fortsett i denne rytmen 🌱",
        "tip_reduce_one": "- Å kutte bare én dag til kan gjøre en merkbar forskjell.",
        "tip_support": "- Å spise før du drikker og lett trening kan støtte hjertehelsen.",
        "tip_try_reduce": "- Prøv å redusere gradvis — små steg teller mest.",
        "disclaimer": "Forbehold: Kun et lærings-demo — ikke medisinske råd. Basert på befolkningsdata, ikke individuelle beregninger.",
    },
}

# ------------------------
# Core models
# ------------------------
def health_gain_alcohol(drinking_days, target_days):
    return max(0, (drinking_days - target_days) * 0.8)

def health_gain_smoking(cigs_now, cigs_goal):
    return max(0, (cigs_now - cigs_goal) / 20 * 96)

# ------------------------
# UI
# ------------------------
st.markdown(f"# <span class='uio-accent'>{S[LANG]['title']}</span>", unsafe_allow_html=True)
st.markdown(S[LANG]["subtitle"])

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.form("inputs"):
        # Basic info
        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age", min_value=15, max_value=90, value=28, step=1)
        with c2:
            st.write("")

        # Alcohol section
        st.markdown("### 🍷 Alcohol")
        drinking_days = st.slider("Current drinking days per week", 0, 7, 5)
        target_days = st.slider("Target drinking days per week", 0, 7, 2)

        # Smoking section
        st.markdown("### 🚬 Smoking")
        cigs_now = st.slider("Current cigarettes per day", 0, 40, 20)
        cigs_goal = st.slider("Target cigarettes per day", 0, 40, 0)

        submitted = st.form_submit_button(S[LANG]["calc"])
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    alcohol_gain = health_gain_alcohol(drinking_days, target_days)
    smoking_gain = health_gain_smoking(cigs_now, cigs_goal)
    total_gain = alcohol_gain + smoking_gain

    st.subheader(S[LANG]["your_gain"])

    # Alcohol result
    st.markdown(
        f"""
        **Nice move!**  
        People who cut down from {drinking_days} to {target_days} drinking days a week tend to live longer —  
        <span class='highlight-number'>🌿 +{alcohol_gain:.1f} months on average</span>
        """, unsafe_allow_html=True,
    )

    # Smoking result
    st.markdown(
        f"""
        **Strong choice!**  
        People who reduce smoking from {cigs_now} to {cigs_goal} cigarettes a day tend to live longer —  
        <span class='highlight-number'>🌿 +{smoking_gain:.0f} months on average</span>
        """, unsafe_allow_html=True,
    )

    # Combined summary
    st.markdown("---")
    st.markdown(
        f"""
        ### 🌱 Combined estimated health gain  
        <span class='highlight-number'>≈ +{total_gain:.0f} months total (population average)</span>
        """, unsafe_allow_html=True,
    )

    # Progress bar
    st.markdown(S[LANG]["lifespan_bar"])
    cap_months = 120
    st.progress(min(total_gain, cap_months) / cap_months)

    # Tips
    st.markdown(S[LANG]["tips"])
    if target_days < drinking_days:
        st.write(S[LANG]["tip_good_start"].format(x=drinking_days, y=target_days))
        if drinking_days - target_days >= 2:
            st.write(S[LANG]["tip_reduce_one"])
        st.write(S[LANG]["tip_support"])
    else:
        st.write(S[LANG]["tip_try_reduce"])

st.markdown("---")
st.caption(S[LANG]["disclaimer"])
