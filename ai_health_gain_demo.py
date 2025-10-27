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
      .highlight-number {
        font-size: 28px; font-weight: 700; color: #2E8B57;
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
    "title": "AI Health Gain — Demo",
    "subtitle": "See how small changes can lead to **visible health gains**. *Educational concept — not medical advice.*",
    "calc": "Calculate health gain",
    "your_gain": "Your estimated gain",
    "lifespan_bar": "**Health lifespan bar**",
    "disclaimer": "Disclaimer: Educational demo only — not medical advice. Parameters are placeholders and will be calibrated with peer-reviewed evidence and local data.",
  },
  "NO": {
    "title": "AI Health Gain — Demo",
    "subtitle": "Se hvordan små endringer kan gi **synlige helseeffekter**. *Kun for læring — ikke medisinske råd.*",
    "calc": "Beregn helseeffekt",
    "your_gain": "Din estimerte gevinst",
    "lifespan_bar": "**Helse-leveår (indikator)**",
    "disclaimer": "Forbehold: Kun et lærings-demo — ikke medisinske råd. Parametere er plassholdere og skal kalibreres mot fagfellevurdert kunnskap og lokale data.",
  }
}

# ------------------------
# Demo: visually enhanced result output
# ------------------------
st.markdown(f"# <span class='uio-accent'>{S[LANG]['title']}</span>", unsafe_allow_html=True)
st.markdown(S[LANG]["subtitle"])

st.header("🍷 Alcohol example")

current = 5
target = 2
months = 4

st.markdown(
    f"""
    **Nice move!**  
    People who cut down from {current} to {target} drinking days a week tend to live longer —  
    <span class='highlight-number'>🌿 +{months} months on average</span>
    """,
    unsafe_allow_html=True,
)

st.markdown(S[LANG]["lifespan_bar"])
progress = min(months, 36) / 36
st.progress(progress)

st.caption(S[LANG]["disclaimer"])