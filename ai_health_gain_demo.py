import streamlit as st

st.set_page_config(page_title="AI Health Gain Demo", page_icon="💡", layout="centered")

st.title("💡 AI Health Gain Demo")

st.markdown("This demo illustrates how lifestyle improvements are associated with health gains based on population-level research.")

# -------------------
# Alcohol Module
# -------------------
st.header("🍷 Alcohol Consumption")
current_drinks = st.slider("Current drinking frequency (times per week)", 0, 7, 5)
target_drinks = st.slider("Target drinking frequency (times per week)", 0, 7, 1)

# Approximation: each weekly reduction ≈ +0.8 months of average life expectancy
alcohol_gain = max(0, (current_drinks - target_drinks) * 0.8)

st.success(f"Good news! In studies, people who reduced drinking like this showed an average health gain equivalent to about **{alcohol_gain:.1f} months** of extra life.")

st.caption("Sources: Global Burden of Disease (GBD) 2023, UK Biobank Lifestyle Study. Based on population-level associations, not individual prediction.")

# -------------------
# Smoking Module
# -------------------
st.header("🚬 Smoking Frequency")
current_smokes = st.slider("Current cigarettes per day", 0, 40, 20)
target_smokes = st.slider("Target cigarettes per day", 0, 40, 0)

# Simplified linear model: 20 → 0 cigarettes ≈ +8 years (96 months)
smoking_gain = max(0, (current_smokes - target_smokes) / 20 * 96)

st.success(f"In studies, people who reduced smoking like this showed an average health gain equivalent to about **{smoking_gain:.0f} months** of extra life.")

st.caption("Sources: GBD 2023, UK Biobank, NHS Longitudinal Study. Population-average associations only.")

# -------------------
# Summary Section
# -------------------
total_gain_months = alcohol_gain + smoking_gain

st.markdown("---")
st.subheader("📈 Summary")
st.write(f"Combined estimated population-average health gain: **{total_gain_months:.1f} months**")

st.info("These results communicate *average associations observed in population studies*. They are **not** individual health predictions or medical advice.")

st.markdown("---")
st.caption("AI Health Gain Demo – for educational and public-health communication purposes.")