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
      .highlight-number { font-size: 28px; font-weight: 700; color: #2E8B57; }
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
    "age": "Age (years)",
    "sex": "Gender",
    "male": "Male",
    "female": "Female",
    "years_drink": "Years of drinking",
    "days_now": "Current drinking days per week",
    "drinks_per": "Average drinks per drinking day",
    "days_goal": "Goal: reduce drinking days to",
    "smoking_now": "Current cigarettes per day",
    "smoking_goal": "Goal: reduce cigarettes per day to",
    "years_smoking": "Years of smoking",
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
    "headline": "If you reduce your drinking days from {now} to {goal} per week, you could gain about +{months} months of healthy life.",
    "headline_smoking": "If you reduce smoking from {now} to {goal} cigarettes per day, you could gain about +{months} months of healthy life.",
    "txt_title": "AI Health Gain – Demo Result",
    "txt_inputs": "Inputs",
    "txt_age": "Age",
    "txt_sex": "Sex",
    "txt_days": "Drinking days (now→goal)",
    "txt_drinks_occ": "Average drinks per drinking day",
    "txt_years": "Years drinking",
    "txt_smoking": "Cigarettes per day (now→goal)",
    "txt_years_smoking": "Years smoking",
    "txt_model": "Model (demo)",
    "txt_rr": "RR now / after",
    "txt_gain": "Healthy life gain"
  },
  "NO": {
    "title": "🌿 AI Health Gain — Demo",
    "subtitle": "Se hvordan små endringer kan gi **synlige helseeffekter**. *Kun for læring — ikke medisinske råd.*",
    "age": "Alder (år)",
    "sex": "Kjønn",
    "male": "Mann",
    "female": "Kvinne",
    "years_drink": "Antall år med alkoholbruk",
    "days_now": "Nåværende drikkedager per uke",
    "drinks_per": "Gjennomsnittlige enheter per drikkedag",
    "days_goal": "Mål: reduser drikkedager til",
    "smoking_now": "Sigaretter per dag (nå)",
    "smoking_goal": "Mål: reduser sigaretter per dag til",
    "years_smoking": "Antall år med røyking",
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
    "headline": "Hvis du reduserer drikkedager fra {now} til {goal} per uke, kan du få omtrent +{months} måneder i god helse.",
    "headline_smoking": "Hvis du reduserer røyking fra {now} til {goal} sigaretter per dag, kan du få omtrent +{months} måneder i god helse.",
    "txt_title": "AI Health Gain – Demoresultat",
    "txt_inputs": "Inndata",
    "txt_age": "Alder",
    "txt_sex": "Kjønn",
    "txt_days": "Drikkedager (nå→mål)",
    "txt_drinks_occ": "Gjennomsnittlige enheter per drikkedag",
    "txt_years": "Antall år med alkoholbruk",
    "txt_smoking": "Sigaretter per dag (nå→mål)",
    "txt_years_smoking": "Antall år med røyking",
    "txt_model": "Modell (demo)",
    "txt_rr": "RR nå / etter",
    "txt_gain": "Gevinst i god helse"
  }
}

# ------------------------
# Core models
# ------------------------
def health_gain_alcohol(age, sex, drinking_days, drinks_per_occ, years_drinking, target_days):
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
  return gain_months

def health_gain_smoking(age, sex, cigs_now, cigs_goal, years_smoking):
  # Linear approximation: 20 -> 0 = +8 years (96 months)
  sex_adj = 0.9 if str(sex).lower() in ["female", "f", "woman", "kvinne"] else 1.0
  age_adj = max(0.5, 1.1 - (age - 20) * 0.01)
  adjust = sex_adj * age_adj
  gain_years = 8.0 * (cigs_now - cigs_goal) / 20.0 * adjust
  gain_years = max(0.0, min(gain_years, 10.0))
  gain_months = round(gain_years * 12)
  return gain_months

# ------------------------
# UI
# ------------------------
st.markdown(f"# <span class='uio-accent'>{S[LANG]['title']}</span>", unsafe_allow_html=True)
st.markdown(S[LANG]["subtitle"])

with st.container():
  st.markdown("<div class='card'>", unsafe_allow_html=True)
  with st.form("inputs"):
    # ── Basic info ───────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
      age = st.number_input(S[LANG]["age"], min_value=15, max_value=90, value=28, step=1)
      sex = st.selectbox(S[LANG]["sex"], [S[LANG]["male"], S[LANG]["female"]])
    with c2:
      years_drinking = st.number_input(S[LANG]["years_drink"], min_value=0, max_value=60, value=5, step=1)
      years_smoking = st.number_input(S[LANG]["years_smoking"], min_value=0, max_value=60, value=5, step=1)

    # ── Alcohol module (separate block) ──────────────────────
    st.markdown("### 🍷 Alcohol")
    drinking_days = st.slider(S[LANG]["days_now"], 0, 7, 4)
    drinks_per_occ = st.slider(S[LANG]["drinks_per"], 0, 10, 2)
    target_days = st.slider(S[LANG]["days_goal"], 0, 7, 2)

    # ── Smoking module (separate block) ──────────────────────
    st.markdown("### 🚬 Smoking")
    cigs_now = st.slider(S[LANG]["smoking_now"], 0, 40, 20)
    cigs_goal = st.slider(S[LANG]["smoking_goal"], 0, 40, 0)

    submitted = st.form_submit_button(S[LANG]["calc"])
  st.markdown("</div>", unsafe_allow_html=True)

if submitted:
  st.subheader(S[LANG]["your_gain"])
  alcohol_gain = health_gain_alcohol(age, sex, drinking_days, drinks_per_occ, years_drinking, target_days)
  smoking_gain = health_gain_smoking(age, sex, cigs_now, cigs_goal, years_smoking)
  total_gain = alcohol_gain + smoking_gain

  # Friendly, emphasized output for Alcohol
  st.markdown(
    f"""
  **Nice move!**  
  People who cut down from {drinking_days} to {target_days} drinking days a week tend to live longer —  
  <span class='highlight-number'>🌿 +{alcohol_gain:.1f} months on average</span>
    """, unsafe_allow_html=True
  ))
  # Friendly, emphasized output for Smoking
  st.markdown(
    f"""
  **Strong choice!**  
  People who reduce smoking from {cigs_now} to {cigs_goal} cigarettes a day tend to live longer —  
  <span class='highlight-number'>🌿 +{smoking_gain:.0f} months on average</span>
    """, unsafe_allow_html=True
  ))

  st.markdown(S[LANG]["lifespan_bar"])
  cap_months = 120
  progress = min(total_gain, cap_months) / cap_months
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
    st.json({"alcohol_gain_months": alcohol_gain, "smoking_gain_months": smoking_gain, "total_gain_months": total_gain})

  st.markdown("---")
  st.markdown(S[LANG]["save_result"])

  unit_months = "months" if LANG == "EN" else "måneder"
  txt = (
    f"{S[LANG]['txt_title']}\n"
    f"Time: {datetime.utcnow().isoformat()}Z\n\n"
    f"Alcohol: {S[LANG]['headline'].format(now=drinking_days, goal=target_days, months=alcohol_gain)}\n"
    f"Smoking: {S[LANG]['headline_smoking'].format(now=cigs_now, goal=cigs_goal, months=smoking_gain)}\n\n"
    f"Total estimated health gain: {total_gain} {unit_months}\n\n"
    f"{S[LANG]['txt_inputs']}:\n"
    f"- {S[LANG]['txt_age']}: {age}\n"
    f"- {S[LANG]['txt_sex']}: {sex}\n"
    f"- {S[LANG]['txt_days']}: {drinking_days} → {target_days}\n"
    f"- {S[LANG]['txt_drinks_occ']}: {drinks_per_occ}\n"
    f"- {S[LANG]['txt_years']}: {years_drinking}\n"
    f"- {S[LANG]['txt_smoking']}: {cigs_now} → {cigs_goal}\n"
    f"- {S[LANG]['txt_years_smoking']}: {years_smoking}\n\n"
    f"{S[LANG]['txt_model']}:\n"
    f"- {S[LANG]['txt_gain']}: {total_gain} {unit_months}\n"
  )
  st.download_button(S[LANG]["download_txt"], txt, file_name="ai_health_gain_result.txt")

  df = pd.DataFrame([{ "alcohol_gain": alcohol_gain, "smoking_gain": smoking_gain, "total_gain": total_gain }])
  csv_buf = io.StringIO()
  df.to_csv(csv_buf, index=False)
  st.download_button(S[LANG]["download_csv"], csv_buf.getvalue(), file_name="ai_health_gain_result.csv")

st.markdown("---")
st.caption(S[LANG]["disclaimer"])
