
import streamlit as st
import io
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Health Gain — Demo (EN/NO)", page_icon="🌿", layout="centered")

# ------------------------
# Minimal CSS for a modern look & top-left language switcher
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
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------
# Language state & strings
# ------------------------
if "lang" not in st.session_state:
  st.session_state["lang"] = "EN"  # default EN

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
    "subtitle": "See how small changes can lead to **visible health gains**. *Educational concept — not medical advice.*",
    "factor_label": "Select lifestyle factor",
    "factor_options": ["🍷 Alcohol", "🚭 Smoking"],
    "age": "Age (years)",
    "sex": "Gender",
    "male": "Male",
    "female": "Female",

    # Alcohol strings
    "alcohol_header": "🍷 Alcohol",
    "years_drink": "Years of drinking",
    "days_now": "Current drinking days per week",
    "drinks_per": "Average drinks per drinking day",
    "days_goal": "Goal: reduce drinking days to",
    "calc": "Calculate health gain",
    "your_gain": "Your estimated gain",
    "lifespan_bar": "**Health lifespan bar**",
    "tips": "### 💬 Gentle tips",
    "tip_good_start": "- Great start — moving from **{x}** to **{y}** days. Keep this pace 🌱",
    "tip_reduce_one": "- If helpful, reduce by 1 day first and build your rhythm.",
    "tip_support": "- Eating before drinking and ~3 workouts/week can further support heart health.",
    "tip_try_reduce": "- Try reducing by 1 day per week first and build a sustainable rhythm.",
    "see_details": "See model details (demo, explainable)",
    "save_result": "### ⬇️ Save your result",
    "download_txt": "Download summary (.txt)",
    "download_csv": "Download data (.csv)",
    "disclaimer": "Disclaimer: Educational demo only — not medical advice. Parameters are placeholders and will be calibrated with peer‑reviewed evidence and local data.",
    "headline_alcohol": "Good news! Reducing drinking days from {now} to {goal} per week is associated with an average health gain of about +{months} months.",
    "txt_title": "AI Health Gain – Demo Result",
    "txt_inputs": "Inputs",
    "txt_age": "Age",
    "txt_sex": "Sex",
    "txt_days": "Drinking days (now→goal)",
    "txt_drinks_occ": "Average drinks per drinking day",
    "txt_years": "Years drinking",
    "txt_model": "Model (demo)",
    "txt_rr": "RR now / after",
    "txt_gain": "Healthy life gain",

    # Smoking strings
    "smoking_header": "🚭 Smoking",
    "years_smoke": "Years of smoking",
    "cigs_now": "Cigarettes per day (now)",
    "cigs_goal": "Cigarettes per day (goal)",
    "headline_smoking": "Good news! Reducing from {now} to {goal} cigarettes per day is associated with an average health gain of about +{months} months."
  },
  "NO": {
    "title": "🌿 AI Health Gain — Demo",
    "subtitle": "Se hvordan små endringer kan gi **synlige helseeffekter**. *Kun for læring — ikke medisinske råd.*",
    "factor_label": "Velg livsstilsfaktor",
    "factor_options": ["🍷 Alkohol", "🚭 Røyking"],
    "age": "Alder (år)",
    "sex": "Kjønn",
    "male": "Mann",
    "female": "Kvinne",

    # Alcohol strings
    "alcohol_header": "🍷 Alkohol",
    "years_drink": "Antall år med alkoholbruk",
    "days_now": "Nåværende drikkedager per uke",
    "drinks_per": "Gjennomsnittlige enheter per drikkedag",
    "days_goal": "Mål: reduser drikkedager til",
    "calc": "Beregn helseeffekt",
    "your_gain": "Din estimerte gevinst",
    "lifespan_bar": "**Helse‑leveår (indikator)**",
    "tips": "### 💬 Enkle råd",
    "tip_good_start": "- God start — fra **{x}** til **{y}** dager. Fortsett i denne rytmen 🌱",
    "tip_reduce_one": "- Om det hjelper, reduser først med 1 dag og bygg vanen gradvis.",
    "tip_support": "- Å spise før man drikker og ~3 økter/uke kan støtte hjertehelsen.",
    "tip_try_reduce": "- Prøv å redusere med 1 dag per uke først og bygg et bærekraftig mønster.",
    "see_details": "Se modell‑detaljer (demo, forklarbar)",
    "save_result": "### ⬇️ Lagre resultatet",
    "download_txt": "Last ned sammendrag (.txt)",
    "download_csv": "Last ned data (.csv)",
    "disclaimer": "Forbehold: Kun et lærings‑demo — ikke medisinske råd. Parametere er plassholdere og skal kalibreres mot fagfellevurdert kunnskap og lokale data.",
    "headline_alcohol": "Gode nyheter! Å redusere drikkedager fra {now} til {goal} per uke er forbundet med en gjennomsnittlig helseeffekt tilsvarende ca. +{months} måneder.",
    "txt_title": "AI Health Gain – Demoresultat",
    "txt_inputs": "Inndata",
    "txt_age": "Alder",
    "txt_sex": "Kjønn",
    "txt_days": "Drikkedager (nå→mål)",
    "txt_drinks_occ": "Gjennomsnittlige enheter per drikkedag",
    "txt_years": "Antall år med alkoholbruk",
    "txt_model": "Modell (demo)",
    "txt_rr": "RR nå / etter",
    "txt_gain": "Gevinst i god helse",

    # Smoking strings
    "smoking_header": "🚭 Røyking",
    "years_smoke": "Antall år med røyking",
    "cigs_now": "Sigaretter per dag (nå)",
    "cigs_goal": "Sigaretter per dag (mål)",
    "headline_smoking": "Gode nyheter! Å redusere fra {now} til {goal} sigaretter per dag er forbundet med en gjennomsnittlig helseeffekt tilsvarende ca. +{months} måneder."
  }
}

# ------------------------
# Core models
# ------------------------
def alcohol_gain_model(age, sex, drinking_days, drinks_per_occ, years_drinking, target_days):
  drinks_per_week_now = drinking_days * drinks_per_occ
  drinks_per_week_after = target_days * drinks_per_occ

  binge_now = 1 if drinks_per_occ >= 5 else 0
  binge_after = binge_now

  a, b, c = 0.02, 0.15, 0.10
  sex_adj = 0.95 if str(sex).lower() in ["female", "f", "woman", "kvinne"] else 1.0
  age_adj = max(0.6, 1.2 - (age - 20) * 0.01)
  adjust = sex_adj * age_adj

  rr_now = 1 + a * drinks_per_week_now + b * binge_now + c * (years_drinking / 20.0)
  rr_after = 1 + a * drinks_per_week_after + b * binge_after + c * (years_drinking / 20.0)

  rr_now = max(rr_now, 0.8)
  rr_after = max(rr_after, 0.8)

  k = 8.0
  gain_years = k * (rr_now - rr_after) / rr_now * adjust

  gain_years = max(0.0, min(gain_years, 3.0))
  gain_months = round(gain_years * 12)

  headline = S[LANG]["headline_alcohol"].format(now=drinking_days, goal=target_days, months=gain_months)
  detail = {
      "factor": "alcohol",
      "age": age, "sex": sex,
      "now_drinks_per_week": drinks_per_week_now,
      "after_drinks_per_week": drinks_per_week_after,
      "rr_now": round(rr_now, 3),
      "rr_after": round(rr_after, 3),
      "gain_years": round(gain_years, 2),
      "gain_months": gain_months
  }
  return headline, detail

def smoking_gain_model(age, sex, cigs_now, cigs_goal, years_smoking):
  # Approximate pop-average mapping:
  # ~1–2 months gained per 1 cigarette/day reduced; cap at 60 months to stay conservative for demo.
  months_per_cig = 1.5
  reduction = max(0, cigs_now - cigs_goal)
  base_months = reduction * months_per_cig

  # Light adjustment by age/sex to keep symmetry with alcohol demo (still population-level, not personal prediction)
  sex_adj = 0.95 if str(sex).lower() in ["female", "f", "woman", "kvinne"] else 1.0
  age_adj = max(0.6, 1.1 - (age - 20) * 0.008)
  years_adj = 1.0 if years_smoking <= 1 else min(1.2, 0.9 + years_smoking / 50.0)

  gain_months = int(round(base_months * sex_adj * age_adj * years_adj))
  gain_months = max(0, min(gain_months, 60))  # cap at 5 years

  detail = {
      "factor": "smoking",
      "age": age, "sex": sex,
      "cigs_now": cigs_now,
      "cigs_goal": cigs_goal,
      "years_smoking": years_smoking,
      "gain_months": gain_months
  }
  headline = S[LANG]["headline_smoking"].format(now=cigs_now, goal=cigs_goal, months=gain_months)
  return headline, detail

# ------------------------
# Header
# ------------------------
st.markdown(f"# <span class='uio-accent'>{S[LANG]['title']}</span>", unsafe_allow_html=True)
st.markdown(S[LANG]["subtitle"])

# Lifestyle factor selection
with st.container():
  st.markdown("<div class='card'>", unsafe_allow_html=True)
  factor = st.selectbox(S[LANG]["factor_label"], S[LANG]["factor_options"], index=0)
  st.markdown("</div>", unsafe_allow_html=True)

# ------------------------
# UI — Alcohol Module
# ------------------------
def alcohol_module():
  with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(S[LANG]["alcohol_header"])
    with st.form("inputs_alcohol"):
      col1, col2 = st.columns(2)
      with col1:
        age = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1, key="age_alc")
        sex = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]], key="sex_alc")
        years_drinking = st.number_input(S[LANG]["years_drink"], min_value=0, max_value=60, value=5, step=1, key="years_alc")
      with col2:
        drinking_days = st.slider(S[LANG]["days_now"], 0, 7, 4, key="days_now_alc")
        drinks_per_occ = st.slider(S[LANG]["drinks_per"], 0, 10, 2, key="drinks_per_alc")
        target_days = st.slider(S[LANG]["days_goal"], 0, 7, 2, key="days_goal_alc")
      submitted = st.form_submit_button(S[LANG]["calc"])
    st.markdown("</div>", unsafe_allow_html=True)

  if submitted:
    st.subheader(S[LANG]["your_gain"])
    headline, detail = alcohol_gain_model(
        age=age, sex=sex, drinking_days=drinking_days,
        drinks_per_occ=drinks_per_occ, years_drinking=years_drinking,
        target_days=target_days
    )
    st.success(headline)

    st.markdown(S[LANG]["lifespan_bar"])
    cap_months = 36
    progress = min(detail["gain_months"], cap_months) / cap_months
    st.progress(progress)

    st.markdown(S[LANG]["tips"])
    if target_days < drinking_days:
      st.write(S[LANG]["tip_good_start"].format(x=drinking_days, y=target_days))
      if drinking_days - target_days >= 2:
        st.write(S[LANG]["tip_reduce_one"])
      st.write(S[LANG]["tip_support"])
    else:
      st.write(S[LANG]["tip_try_reduce"])

    with st.expander(S[LANG]["see_details"]):
      st.json(detail)

    # ---- Downloads ----
    st.markdown("---")
    st.markdown(S[LANG]["save_result"])

    unit_months = "months" if LANG == "EN" else "måneder"
    txt = (
      f"{S[LANG]['txt_title']}
"
      f"Time: {datetime.utcnow().isoformat()}Z

"
      f"{headline}

"
      f"{S[LANG]['txt_inputs']}:
"
      f"- {S[LANG]['txt_age']}: {detail['age']}
"
      f"- {S[LANG]['txt_sex']}: {detail['sex']}
"
      f"- {S[LANG]['txt_days']}: {drinking_days} → {target_days}
"
      f"- {S[LANG]['txt_drinks_occ']}: {drinks_per_occ}
"
      f"- {S[LANG]['txt_years']}: {years_drinking}

"
      f"{S[LANG]['txt_model']}:
"
      f"- {S[LANG]['txt_rr']}: {detail['rr_now']} / {detail['rr_after']}
"
      f"- {S[LANG]['txt_gain']}: {detail['gain_months']} {unit_months}
"
    )
    st.download_button(S[LANG]["download_txt"], txt, file_name="ai_health_gain_result_alcohol.txt")

    df = pd.DataFrame([detail])
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button(S[LANG]["download_csv"], csv_buf.getvalue(), file_name="ai_health_gain_result_alcohol.csv")

# ------------------------
# UI — Smoking Module
# ------------------------
def smoking_module():
  with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(S[LANG]["smoking_header"])
    with st.form("inputs_smoking"):
      col1, col2 = st.columns(2)
      with col1:
        age = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1, key="age_sm")
        sex = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]], key="sex_sm")
        years_smoking = st.number_input(S[LANG]["years_smoke"], min_value=0, max_value=60, value=5, step=1, key="years_sm")
      with col2:
        cigs_now = st.slider(S[LANG]["cigs_now"], 0, 40, 10, key="cigs_now")
        cigs_goal = st.slider(S[LANG]["cigs_goal"], 0, cigs_now, 0, key="cigs_goal")
      submitted = st.form_submit_button(S[LANG]["calc"])
    st.markdown("</div>", unsafe_allow_html=True)

  if submitted:
    st.subheader(S[LANG]["your_gain"])
    headline, detail = smoking_gain_model(
        age=age, sex=sex, cigs_now=cigs_now, cigs_goal=cigs_goal, years_smoking=years_smoking
    )
    st.success(headline)

    st.markdown(S[LANG]["lifespan_bar"])
    cap_months = 60  # larger cap for smoking
    progress = min(detail["gain_months"], cap_months) / cap_months
    st.progress(progress)

    # Simple tips for smoking
    st.markdown(S[LANG]["tips"])
    if cigs_goal < cigs_now:
      st.write("- Stepwise reduction or complete cessation both show strong benefits in studies.")
      st.write("- Consider support: nicotine replacement, counseling, or apps can double success rates.")
    else:
      st.write("- Try reducing by 1–2 cigarettes/day first and build from there.")

    with st.expander(S[LANG]["see_details"]):
      st.json(detail)

    # ---- Downloads ----
    st.markdown("---")
    st.markdown(S[LANG]["save_result"])

    unit_months = "months" if LANG == "EN" else "måneder"
    txt = (
      f"{S[LANG]['txt_title']}
"
      f"Time: {datetime.utcnow().isoformat()}Z

"
      f"{headline}

"
      f"{S[LANG]['txt_inputs']}:
"
      f"- {S[LANG]['txt_age']}: {detail['age']}
"
      f"- {S[LANG]['txt_sex']}: {detail['sex']}
"
      f"- {S[LANG]['years_smoke'] if 'years_smoke' in S[LANG] else 'Years smoking'}: {years_smoking}
"
      f"- {S[LANG]['cigs_now']}: {detail['cigs_now']}
"
      f"- {S[LANG]['cigs_goal']}: {detail['cigs_goal']}

"
      f"{S[LANG]['txt_model']}:
"
      f"- {S[LANG]['txt_gain']}: {detail['gain_months']} {unit_months}
"
    )
    st.download_button(S[LANG]["download_txt"], txt, file_name="ai_health_gain_result_smoking.txt")

    df = pd.DataFrame([detail])
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button(S[LANG]["download_csv"], csv_buf.getvalue(), file_name="ai_health_gain_result_smoking.csv")

# ------------------------
# Render the selected module
# ------------------------
if (LANG == "EN" and factor == "🍷 Alcohol") or (LANG == "NO" and factor == "🍷 Alkohol"):
  alcohol_module()
else:
  smoking_module()

st.markdown("---")
st.caption(S[LANG]["disclaimer"])
