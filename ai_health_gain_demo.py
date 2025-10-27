import streamlit as st

st.set_page_config(page_title="AI Health Gain — Demo (EN/NO)", page_icon="🌿", layout="centered")

# ------------------------
# CSS styling
# ------------------------
st.markdown(
    """
    <style>
      html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      }
      .highlight-number { font-size: 28px; font-weight: 700; color: #2E8B57; }
      .card {
        border: 1px solid rgba(0,0,0,0.07);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 1px 10px rgba(0,0,0,0.06);
        background: #fff;
        margin-bottom: 24px;
      }
    </style>
    """, unsafe_allow_html=True,
)

# ------------------------
# Language toggle
# ------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"

choice = st.radio("Language", ["EN", "NO"], horizontal=True)
st.session_state["lang"] = choice
LANG = st.session_state["lang"]

# ------------------------
# Text dictionary
# ------------------------
S = {
    "EN": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Explore how small lifestyle changes can make a visible difference. *Educational demo — not medical advice.*",
        "calc": "Calculate health gain",
        "alcohol_title": "🍷 Alcohol",
        "smoking_title": "🚬 Smoking",
        "lifespan_bar": "**Health lifespan indicator**",
        "tips": "### 💬 Gentle tips",
        "tip_good_start": "- Great start — moving from **{x}** to **{y}** days. Keep this pace 🌱",
        "tip_reduce_one": "- Reducing just one more day can already make a real difference.",
        "tip_support": "- Eating before drinking and light exercise can further support your heart health.",
        "tip_try_reduce": "- Try reducing gradually — small steps matter most.",
        "disclaimer": "Disclaimer: Based on population averages, not individual predictions.",
    },
    "NO": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Små endringer kan gi **store helseeffekter**. *Kun for læring — ikke medisinske råd.*",
        "calc": "Beregn helseeffekt",
        "alcohol_title": "🍷 Alkohol",
        "smoking_title": "🚬 Røyking",
        "lifespan_bar": "**Helseindikator (gjennomsnitt)**",
        "tips": "### 💬 Enkle råd",
        "tip_good_start": "- God start — fra **{x}** til **{y}** dager. Fortsett i denne rytmen 🌱",
        "tip_reduce_one": "- Å kutte bare én dag til kan gjøre en merkbar forskjell.",
        "tip_support": "- Å spise før du drikker og lett trening kan støtte hjertehelsen.",
        "tip_try_reduce": "- Prøv å redusere gradvis — små steg teller mest.",
        "disclaimer": "Forbehold: Basert på befolkningsdata, ikke individuelle beregninger.",
    }
}

# ------------------------
# Calculation functions
# ------------------------
def health_gain_alcohol(drinking_days, target_days):
    return max(0, (drinking_days - target_days) * 0.8)

def health_gain_smoking(cigs_now, cigs_goal):
    return max(0, (cigs_now - cigs_goal) / 20 * 96)

# ------------------------
# Header
# ------------------------
st.markdown(f"# {S[LANG]['title']}")
st.markdown(S[LANG]["subtitle"])

# ========================
# 🍷 Alcohol Module
# ========================
st.markdown(f"## {S[LANG]['alcohol_title']}")
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    drinking_days = st.slider("Current drinking days per week", 0, 7, 5)
    target_days = st.slider("Target drinking days per week", 0, 7, 2)
    calc_alcohol = st.button(S[LANG]["calc"] + " (Alcohol)")
    st.markdown("</div>", unsafe_allow_html=True)

if calc_alcohol:
    alcohol_gain = health_gain_alcohol(drinking_days, target_days)

    st.markdown(
        f"""
        **Nice move!**  
        People who cut down from {drinking_days} to {target_days} drinking days a week tend to live longer —  
        <span class='highlight-number'>🌿 +{alcohol_gain:.1f} months on average</span>
        """, unsafe_allow_html=True,
    )

    st.markdown(S[LANG]["lifespan_bar"])
    st.progress(min(alcohol_gain, 36) / 36)

    st.markdown(S[LANG]["tips"])
    if target_days < drinking_days:
        st.write(S[LANG]["tip_good_start"].format(x=drinking_days, y=target_days))
        if drinking_days - target_days >= 2:
            st.write(S[LANG]["tip_reduce_one"])
        st.write(S[LANG]["tip_support"])
    else:
        st.write(S[LANG]["tip_try_reduce"])

# ========================
# 🚬 Smoking Module
# ========================
st.markdown(f"## {S[LANG]['smoking_title']}")
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    cigs_now = st.slider("Current cigarettes per day", 0, 40, 20)
    cigs_goal = st.slider("Target cigarettes per day", 0, 40, 0)
    calc_smoking = st.button(S[LANG]["calc"] + " (Smoking)")
    st.markdown("</div>", unsafe_allow_html=True)

if calc_smoking:
    smoking_gain = health_gain_smoking(cigs_now, cigs_goal)

    st.markdown(
        f"""
        **Strong choice!**  
        People who reduce smoking from {cigs_now} to {cigs_goal} cigarettes a day tend to live longer —  
        <span class='highlight-number'>🌿 +{smoking_gain:.0f} months on average</span>
        """, unsafe_allow_html=True,
    )

    st.markdown(S[LANG]["lifespan_bar"])
    st.progress(min(smoking_gain, 96) / 96)

    st.markdown(S[LANG]["tips"])
    if cigs_goal < cigs_now:
        st.write(S[LANG]["tip_good_start"].format(x=cigs_now, y=cigs_goal))
        if cigs_now - cigs_goal >= 5:
            st.write(S[LANG]["tip_reduce_one"])
        st.write(S[LANG]["tip_support"])
    else:
        st.write(S[LANG]["tip_try_reduce"])

# Footer
st.markdown("---")
st.caption(S[LANG]["disclaimer"])
