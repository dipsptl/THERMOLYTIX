import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# ===== PAGE SETTINGS =====
st.set_page_config(page_title="Cooling Tower AI", layout="wide")

# ===== BACKGROUND =====
def set_bg():
    try:
        with open("bg.jpg", "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
        }}

        .section-title {{
            color: #FFD580;
            font-size: 22px;
            font-weight: 600;
        }}
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

set_bg()

# ===== ANIMATED TITLE =====

st.markdown("""
<style>
@keyframes spin {
  0% {transform: rotate(0deg);}
  100% {transform: rotate(360deg);}
}

.gear1 {
  display: inline-block;
  font-size: 42px;
  color: #FF8C00;
  animation: spin 6s linear infinite;
  vertical-align: middle;
}

.gear2 {
  display: inline-block;
  font-size: 28px;
  color: black;
  margin-left: -18px;
  animation: spin 4s linear infinite;
  vertical-align: middle;
}

.title-text {
  color:#FF8C00;
  font-size:40px;
  font-weight:700;
  margin-left:12px;
  vertical-align: middle;
}
</style>

<div style="text-align:center; margin-top:-50px;">
  <span class="gear1">⚙️</span>
  <span class="gear2">⚙️</span>
  <span class="title-text">
    Cooling Tower Gear Temp. AI Dashboard
  </span>
</div>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# ===== LAYOUT WITH GAP =====
left, gap, right = st.columns([1, 0.15, 1])

# ===== LEFT SIDE =====
with left:
    st.markdown("<br><br>", unsafe_allow_html=True)
   
    st.markdown('<div class="section-title">⚙️ Enter Parameters</div>', unsafe_allow_html=True)

    load = st.slider("Load", 50, 100)
    temp = st.slider("🌡️ Ambient Temp", 25, 50)
    rpm = st.slider("⚡ RPM", 1200, 1800)
    oil = st.slider("🛢️ Oil Condition", 40, 100)

# ===== RIGHT SIDE =====
with right:
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Prediction Summary</div>', unsafe_allow_html=True)
    
    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <h2 style="color:white;">
        {pred_value:.1f}
        <span style="font-size:18px;">°C</span>
    </h2>
    """, unsafe_allow_html=True)

    if pred_value > 90:
        st.error("🔴 Danger")
    elif pred_value > 80:
        st.warning("🟠 Warning")
    else:
        st.success("🟢 Safe")

    st.write("")   # 👈 clean gap

    st.markdown('<div class="section-title">💡 Suggestions</div>', unsafe_allow_html=True)
    
    st.write(" ") 
    
    if rpm > 1500:
        st.warning("Reduce RPM to control heat")

    if oil < 60:
        st.warning("Oil condition poor – maintenance needed")

    if load > 75:
        st.warning("High load – reduce load")

    if temp > 35:
        st.warning("High ambient temp – improve cooling")

# ===== GRAPHS =====
st.markdown("---")
st.markdown('<div class="section-title">📈 Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.scatter(data['Load'], data['Temperature'])
    ax1.set_xlabel("Load")
    ax1.set_ylabel("Temperature")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.scatter(data['RPM'], data['Temperature'])
    ax2.set_xlabel("RPM")
    ax2.set_ylabel("Temperature")
    st.pyplot(fig2)

# ===== PDF FUNCTION =====
def create_pdf(load, temp, rpm, oil, result):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(file.name)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Cooling Tower Report", styles['Title']))
    content.append(Paragraph(f"Load: {load}", styles['Normal']))
    content.append(Paragraph(f"Ambient Temp: {temp}", styles['Normal']))
    content.append(Paragraph(f"RPM: {rpm}", styles['Normal']))
    content.append(Paragraph(f"Oil Condition: {oil}", styles['Normal']))
    content.append(Paragraph(f"Temperature: {result:.2f} °C", styles['Normal']))

    doc.build(content)
    return file.name

# ===== DOWNLOAD =====
st.markdown("---")

if st.button("📁 Download PDF Report"):
    pdf_file = create_pdf(load, temp, rpm, oil, pred_value)

    with open(pdf_file, "rb") as f:
        st.download_button("Download Report", f, file_nam
