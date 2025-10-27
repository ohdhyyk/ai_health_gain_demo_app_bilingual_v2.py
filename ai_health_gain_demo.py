import streamlit as st
import io
import pandas as pd

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
        padding: 16px 18px;
        margin-bottom: 20px;
        box-shadow: 0 1px 8px rgba(0,0,0,0.05);
      }
      .highlight-number {
        font-size: 28px;
        font-weight: 800;
        color: #2E8B57;
      }
      .block-container { padding-top: 1.2rem; }
      .stSlider { margin-top: 0 !important; }
    </style>
    """, unsafe_allow_html=True,
)

# ------------------------
# Language switch
# ------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"

LANG = st.radio("Language", ["EN", "NO"], horizontal=True, index=0 if st.session_state["lang"]=="EN" else 1)
st.session_state["lang"] = LANG

S = {
    "EN": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "See how small lifestyle changes can add up to visible health gains. *Educational demo — not medical advice.*",
        "calc": "Calculate health gain",
        "alcohol_title": "🍷 Alcohol",
        "smoking_title": "🚬 Smoking",
        "age": "Age (years)",
        "sex": "Gender",
        "male": "Male",
        "female": "Female",
        "years_drink": "Years of drinking",
        "years_smoking": "Years of smoking",
        "days_now": "Current drinking days per week",
        "drinks_per": "Average drinks per drinking day",
        "days_goal": "Goal: reduce to days per week",
        "smoking_now": "Current cigarettes per day",
        "smoking_goal": "Goal: reduce to cigarettes per day",
        "calc_button_a": "Calculate health gain (Alcohol)",
        "calc_button_s": "Calculate health gain (Smoking)",
        "gain_a_text": "**Nice move!**  
People who cut down from {x} to {y} drinking days a week tend to live longer —  
<span class='highlight-number'>🌿 +{m} months on average</span>",
        "gain_s_text": "**Strong choice!**  
People who reduce smoking from {x} to {y} cigarettes a day tend to live longer —  
<span class='highlight-number'>🌿 +{m} months on average</span>",
        "your_gain": "Your estimated gain",
        "lifespan_bar": "**Health lifespan indicator**",
        "tips": "### 💬 Gentle tips",
        "tip_good_start": "- Great start — moving from **{x}** to **{y}**. Keep this pace 🌱",
        "tip_reduce_one": "- Reducing just a bit more can already make a real difference.",
        "tip_support": "- Eating before drinking and light exercise can support heart health.",
        "tip_try_reduce": "- Try reducing gradually — small steps matter most.",
        "save_result": "### ⬇️ Save your result",
        "download_txt": "Download summary (.txt)",
        "download_csv": "Download data (.csv)",
        "disclaimer": "Disclaimer: Educational demo only — not medical advice. Based on population averages, not individual predictions.",
    },
    "NO": {
        "title": "🌿 AI Health Gain — Demo",
        "subtitle": "Se hvordan små endringer kan gi tydelige helseeffekter. *Kun for læring — ikke medisinske råd.*",
        "calc": "Beregn helseeffekt",
        "alcohol_title": "🍷 Alkohol",
        "smoking_title": "🚬 Røyking",
        "age": "Alder (år)",
        "sex": "Kjønn",
        "male": "Mann",
        "female": "Kvinne",
        "years_drink": "Antall år med alkoholbruk",
        "years_smoking": "Antall år med røyking",
        "days_now": "Drikkedager per uke (nå)",
        "drinks_per": "Gjennomsnittlige enheter per drikkedag",
        "days_goal": "Mål: reduser til dager per uke",
        "smoking_now": "Sigaretter per dag (nå)",
        "smoking_goal": "Mål: reduser til sigaretter per dag",
        "calc_button_a": "Beregn helseeffekt (Alkohol)",
        "calc_button_s": "Beregn helseeffekt (Røyking)",
        "gain_a_text": "**Godt valg!**  
De som reduserer fra {x} til {y} drikkedager i uka lever som regel litt lengre —  
<span class='highlight-number'>🌿 +{m} måneder i snitt</span>",
        "gain_s_text": "**Sterkt valg!**  
De som reduserer røyking fra {x} til {y} sigaretter per dag lever som regel litt lengre —  
<span class='highlight-number'>🌿 +{m} måneder i snitt</span>",
        "your_gain": "Din estimerte gevinst",
        "lifespan_bar": "**Helseindikator (gjennomsnitt)**",
        "tips": "### 💬 Enkle råd",
        "tip_good_start": "- God start — fra **{x}** til **{y}**. Fortsett i denne rytmen 🌱",
        "tip_reduce_one": "- Litt mindre kan allerede gi merkbar effekt.",
        "tip_support": "- Å spise før man drikker og lett trening kan støtte hjertehelsen.",
        "tip_try_reduce": "- Prøv å redusere gradvis — små steg teller mest.",
        "save_result": "### ⬇️ Lagre resultatet",
        "download_txt": "Last ned sammendrag (.txt)",
        "download_csv": "Last ned data (.csv)",
        "disclaimer": "Forbehold: Kun et lærings-demo — ikke medisinske råd. Basert på befolkningsdata, ikke individuelle beregninger.",
    }
}

# ------------------------
# Models
# ------------------------
def health_gain_alcohol(drinking_days, drinks_per_occ, target_days):
    return round(max(0, (drinking_days - target_days) * 0.8), 1)

def health_gain_smoking(cigs_now, cigs_goal):
    return int(round(max(0, (cigs_now - cigs_goal) / 20 * 96)))

# ------------------------
# Header
# ------------------------
st.markdown(f"# {S[LANG]['title']}")
st.markdown(S[LANG]["subtitle"])

# ========================
# 🍷 Alcohol Module
# ========================
st.markdown(f"## {S[LANG]['alcohol_title']}")
st.markdown("<div class='card'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1)
    sex = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]])
    years_drink = st.number_input(S[LANG]["years_drink"], min_value=0, max_value=60, value=5, step=1)
with col2:
    drinking_days = st.slider(S[LANG]["days_now"], 0, 7, 5)
    drinks_per = st.slider(S[LANG]["drinks_per"], 0, 10, 2)
    target_days = st.slider(S[LANG]["days_goal"], 0, 7, 2)

calc_a = st.button(S[LANG]["calc_button_a"])
st.markdown("</div>", unsafe_allow_html=True)

if calc_a:
    alcohol_gain = health_gain_alcohol(drinking_days, drinks_per, target_days)
    st.subheader(S[LANG]["your_gain"])
    st.markdown(S[LANG]["gain_a_text"].format(x=drinking_days, y=target_days, m=alcohol_gain), unsafe_allow_html=True)
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

    st.markdown("---")
    st.markdown(S[LANG]["save_result"])
    txt_a = f"Alcohol module result: +{alcohol_gain} months"
    st.download_button(S[LANG]["download_txt"], txt_a, file_name="alcohol_result.txt")
    df_a = pd.DataFrame([{ "alcohol_gain": alcohol_gain }])
    buf_a = io.StringIO()
    df_a.to_csv(buf_a, index=False)
    st.download_button(S[LANG]["download_csv"], buf_a.getvalue(), file_name="alcohol_result.csv")

# ========================
# 🚬 Smoking Module
# ========================
st.markdown(f"## {S[LANG]['smoking_title']}")
st.markdown("<div class='card'>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    age_s = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1, key="age_s")
    sex_s = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]], key="sex_s")
    years_smoking = st.number_input(S[LANG]["years_smoking"], min_value=0, max_value=60, value=5, step=1, key="ys")
with col4:
    cigs_now = st.slider(S[LANG]["smoking_now"], 0, 40, 20, key="sn")
    cigs_goal = st.slider(S[LANG]["smoking_goal"], 0, 40, 0, key="sg")

calc_s = st.button(S[LANG]["calc_button_s"])
st.markdown("</div>", unsafe_allow_html=True)

if calc_s:
    smoking_gain = health_gain_smoking(cigs_now, cigs_goal)
    st.subheader(S[LANG]["your_gain"])
    st.markdown(S[LANG]["gain_s_text"].format(x=cigs_now, y=cigs_goal, m=smoking_gain), unsafe_allow_html=True)
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

    st.markdown("---")
    st.markdown(S[LANG]["save_result"])
    txt_s = f"Smoking module result: +{smoking_gain} months"
    st.download_button(S[LANG]["download_txt"], txt_s, file_name="smoking_result.txt")
    df_s = pd.DataFrame([{ "smoking_gain": smoking_gain }])
    buf_s = io.StringIO()
    df_s.to_csv(buf_s, index=False)
    st.download_button(S[LANG]["download_csv"], buf_s.getvalue(), file_name="smoking_result.csv")

# ------------------------
# Footer Disclaimer
# ------------------------
st.markdown("---")
st.caption(S[LANG]["disclaimer"])
