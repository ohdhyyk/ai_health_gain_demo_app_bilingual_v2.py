import streamlit as st

st.set_page_config(page_title="AI Health Gain — Demo (EN/NO)", page_icon="🌿", layout="centered")

# ------------------------
# CSS (light theme, compact cards, no extra white gaps)
# ------------------------
st.markdown(
    """
    <style>
      html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      }
      .card {
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 14px;
        padding: 14px 16px;
        margin: 10px 0 18px 0;
        box-shadow: 0 1px 8px rgba(0,0,0,0.05);
      }
      .section-title {
        margin: 0 0 6px 2px;
      }
      .highlight-number {
        font-size: 28px;
        font-weight: 800;
        color: #2E8B57;
      }
      .block-container { padding-top: 1.2rem; }
      .stSlider { margin-top: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------
# Language
# ------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
LANG = st.radio("Language", ["EN", "NO"], horizontal=True, index=0 if st.session_state["lang"]=="EN" else 1)
st.session_state["lang"] = LANG

S = {
    "EN": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Small lifestyle changes can make a real difference. *Educational demo — not medical advice.*",
        "calc": "Calculate health gain",
        "alcohol_title": "🍷 Alcohol",
        "smoking_title": "🚬 Smoking",
        "age": "Age (years)",
        "sex": "Gender",
        "male": "Male",
        "female": "Female",
        "years_drink": "Years of drinking",
        "years_smoke": "Years of smoking",
        "days_now": "Current drinking days / week",
        "drinks_per": "Average drinks per drinking day",
        "days_goal": "Goal: drinking days / week",
        "cigs_now": "Current cigarettes / day",
        "cigs_goal": "Goal: cigarettes / day",
        "your_gain": "Your estimated gain",
        "lifespan_bar": "**Health lifespan indicator**",
        "tips": "### 💬 Gentle tips",
        "tip_good_start": "- Great start — moving from **{x}** to **{y}**. Keep this pace 🌱",
        "tip_reduce_one": "- Reducing just a bit more can already make a real difference.",
        "tip_support": "- Eating before drinking and light exercise can support heart health.",
        "tip_try_reduce": "- Try reducing gradually — small steps matter most.",
        "disclaimer": "Disclaimer: Educational demo only — not medical advice. Based on population averages, not individual predictions."
    },
    "NO": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Små endringer kan gi tydelige helseeffekter. *Kun for læring — ikke medisinske råd.*",
        "calc": "Beregn helseeffekt",
        "alcohol_title": "🍷 Alkohol",
        "smoking_title": "🚬 Røyking",
        "age": "Alder (år)",
        "sex": "Kjønn",
        "male": "Mann",
        "female": "Kvinne",
        "years_drink": "Antall år med alkoholbruk",
        "years_smoke": "Antall år med røyking",
        "days_now": "Drikkedager per uke (nå)",
        "drinks_per": "Gjennomsnittlige enheter per drikkedag",
        "days_goal": "Mål: drikkedager per uke",
        "cigs_now": "Sigaretter per dag (nå)",
        "cigs_goal": "Mål: sigaretter per dag",
        "your_gain": "Din estimerte gevinst",
        "lifespan_bar": "**Helseindikator (gjennomsnitt)**",
        "tips": "### 💬 Enkle råd",
        "tip_good_start": "- God start — fra **{x}** til **{y}**. Fortsett i denne rytmen 🌱",
        "tip_reduce_one": "- Litt mindre kan allerede gi merkbar effekt.",
        "tip_support": "- Å spise før man drikker og lett trening kan støtte hjertehelsen.",
        "tip_try_reduce": "- Reduser gradvis — små steg teller mest.",
        "disclaimer": "Forbehold: Kun et lærings-demo — ikke medisinske råd. Basert på befolkningsdata, ikke individuelle beregninger."
    }
}

# ------------------------
# Models (population-average approximations)
# ------------------------

def health_gain_alcohol(drinking_days, drinks_per_occ, target_days):
    delta_days = max(0, drinking_days - target_days)
    return round(delta_days * 0.8, 1)


def health_gain_smoking(cigs_now, cigs_goal):
    delta_cigs = max(0, cigs_now - cigs_goal)
    return int(round(delta_cigs / 20 * 96))

# ------------------------
# Header
# ------------------------
st.markdown(f"# {S[LANG]['title']}")
st.markdown(S[LANG]["subtitle"])

# ========================
# 🍷 Alcohol module (independent)
# ========================
st.markdown(f"## {S[LANG]['alcohol_title']}")
st.markdown("<div class='card'>", unsafe_allow_html=True)
col_left, col_right = st.columns([1,1])
with col_left:
    age_a = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1, key="age_a")
    sex_a = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]], key="sex_a")
    years_drink_a = st.number_input(S[LANG]["years_drink"], min_value=0, max_value=60, value=5, step=1, key="yd_a")
with col_right:
    d_now = st.slider(S[LANG]["days_now"], 0, 7, 5, key="d_now_a")
    drinks_per = st.slider(S[LANG]["drinks_per"], 0, 10, 2, key="dppd_a")
    d_goal = st.slider(S[LANG]["days_goal"], 0, 7, 2, key="d_goal_a")

calc_alcohol = st.button(S[LANG]["calc"] + " (Alcohol)")
st.markdown("</div>", unsafe_allow_html=True)

if calc_alcohol:
    gain_a = health_gain_alcohol(d_now, drinks_per, d_goal)
    st.markdown(
        f"""
**Nice move!**  
People who cut down from {d_now} to {d_goal} drinking days a week tend to live longer —  
<span class='highlight-number'>🌿 +{gain_a:.1f} months on average</span>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(S[LANG]["lifespan_bar"])
    st.progress(min(gain_a, 36) / 36)
    st.markdown(S[LANG]["tips"])
    if d_goal < d_now:
        st.write(S[LANG]["tip_good_start"].format(x=d_now, y=d_goal))
        if d_now - d_goal >= 2:
            st.write(S[LANG]["tip_reduce_one"])
        st.write(S[LANG]["tip_support"])
    else:
        st.write(S[LANG]["tip_try_reduce"])

# ========================
# 🚬 Smoking module (independent)
# ========================
st.markdown(f"## {S[LANG]['smoking_title']}")
st.markdown("<div class='card'>", unsafe_allow_html=True)
col_left_s, col_right_s = st.columns([1,1])
with col_left_s:
    age_s = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1, key="age_s")
    sex_s = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]], key="sex_s")
    years_smoke_s = st.number_input(S[LANG]["years_smoke"], min_value=0, max_value=60, value=5, step=1, key="ys_s")
with col_right_s:
    c_now = st.slider(S[LANG]["cigs_now"], 0, 40, 20, key="c_now_s")
    c_goal = st.slider(S[LANG]["cigs_goal"], 0, 40, 0, key="c_goal_s")

calc_smoking = st.button(S[LANG]["calc"] + " (Smoking)")
st.markdown("</div>", unsafe_allow_html=True)

if calc_smoking:
    gain_s = health_gain_smoking(c_now, c_goal)
    st.markdown(
        f"""
**Strong choice!**  
People who reduce smoking from {c_now} to {c_goal} cigarettes a day tend to live longer —  
<span class='highlight-number'>🌿 +{gain_s:d} months on average</span>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(S[LANG]["lifespan_bar"])
    st.progress(min(gain_s, 96) / 96)
    st.markdown(S[LANG]["tips"])
    if c_goal < c_now:
        st.write(S[LANG]["tip_good_start"].format(x=c_now, y=c_goal))
        if c_now - c_goal >= 5:
            st.write(S[LANG]["tip_reduce_one"])
        st.write(S[LANG]["tip_support"])
    else:
        st.write(S[LANG]["tip_try_reduce"])

# ------------------------
# Footer Disclaimer
# ------------------------
st.markdown("---")
st.caption(S[LANG]["disclaimer"])
