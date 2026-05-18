import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
import tempfile

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="THERMOLYTIX AI Dashboard",
    layout="wide"
)

# =====================================================
# IMAGE LOAD
# =====================================================

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("bg.jpg")
logo = get_base64("logo.png")

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 0.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1500px;
}}

header {{
    visibility:hidden;
}}

#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

.main-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(6px);
    margin-bottom: 18px;
}}

.small-card {{
    background: rgba(0,0,0,0.60);
    border-radius: 15px;
    padding: 15px;
}}

.logo-img {{
    width: 340px;
    margin-top: -10px;
}}

.title-orange {{
    color: #ff8800;
    font-size: 18px;
    font-weight: 700;
}}

.big-number {{
    font-size: 55px;
    font-weight: 800;
    color: white;
}}

.safe-box {{
    background: #006b28;
    border-radius: 10px;
    padding: 12px;
    color: #67ff99;
    font-size: 22px;
    font-weight: 700;
}}

.warn-box {{
    background: rgba(255,180,0,0.12);
    border: 1px solid rgba(255,180,0,0.2);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    color: #ffd76a;
    font-size: 15px;
}}

.system-box {{
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,140,0,0.3);
    border-radius: 12px;
    padding: 10px 18px;
    color: white;
    font-size: 16px;
    text-align: center;
    width: 230px;
    margin-left: auto;
}}

.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg,#ff8800,#00cfff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 18px;
    font-weight: 700;
}}

.graph-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 18px;
    padding: 15px;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

top1, top2 = st.columns([5,1])

with top1:
    st.markdown(f"""
    <img class="logo-img"
    src="data:image/png;base64,{logo}">
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="system-box">
    🟢 System Operational
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =====================================================
# MAIN SECTION
# =====================================================

left, right = st.columns([1,1])

# =====================================================
# LEFT SIDE
# =====================================================

with left:

    st.markdown("""
    <div class="main-card">

    <h1 style="color:white;">
    AI Dashboard
    </h1>

    <p style="color:#d8d8d8; font-size:18px;">
    Enter parameters to get AI-powered temperature predictions and system insights.
    </p>

    <div class="title-orange">
    ⚙️ Enter Parameters
    </div>

    </div>
    """, unsafe_allow_html=True)

    load = st.slider("Load", 50, 100, 70)
    temp = st.slider("Ambient Temp", 25, 50, 30)
    rpm = st.slider("RPM", 1200, 1800, 1450)
    oil = st.slider("Oil Condition", 40, 100, 75)

    st.button("PREDICT TEMPERATURE")

# =====================================================
# RIGHT SIDE
# =====================================================

with right:

    pred_value = model.predict([[load,temp,rpm,oil]])[0]

    st.markdown(f"""
    <div class="main-card">

    <div class="title-orange">
    📊 Prediction Summary
    </div>

    <div class="big-number">
    {pred_value:.1f} °C
    </div>

    <div class="safe-box">
    🟢 Safe
    </div>

    <br>

    <div class="title-orange">
    💡 Suggestions
    </div>

    <br>

    """, unsafe_allow_html=True)

    if rpm > 1400:
        st.markdown("""
        <div class="warn-box">
        ⚠️ Reduce RPM to control heat
        </div>
        """, unsafe_allow_html=True)

    if oil < 80:
        st.markdown("""
        <div class="warn-box">
        ⚠️ Oil condition poor – maintenance needed
        </div>
        """, unsafe_allow_html=True)

    if load > 65:
        st.markdown("""
        <div class="warn-box">
        ⚠️ High load – reduce load
        </div>
        """, unsafe_allow_html=True)

    if temp > 28:
        st.markdown("""
        <div class="warn-box">
        ⚠️ High ambient temp – improve cooling
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYSIS
# =====================================================

st.markdown("""
<div class="main-card">
<div class="title-orange">
📈 Analysis
</div>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2)

# =====================================================
# GRAPH 1
# =====================================================

with g1:

    fig1, ax1 = plt.subplots(figsize=(6,3.5))

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=60
    )

    ax1.set_facecolor("#050b18")
    fig1.patch.set_facecolor("#050b18")

    ax1.set_title(
        "Temperature vs Load",
        color="white"
    )

    ax1.set_xlabel("Load (%)", color="white")
    ax1.set_ylabel("Temperature (°C)", color="white")

    ax1.tick_params(colors='white')

    for spine in ax1.spines.values():
        spine.set_color("white")

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# GRAPH 2
# =====================================================

with g2:

    fig2, ax2 = plt.subplots(figsize=(6,3.5))

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=60
    )

    ax2.set_facecolor("#050b18")
    fig2.patch.set_facecolor("#050b18")

    ax2.set_title(
        "Temperature vs RPM",
        color="white"
    )

    ax2.set_xlabel("RPM", color="white")
    ax2.set_ylabel("Temperature (°C)", color="white")

    ax2.tick_params(colors='white')

    for spine in ax2.spines.values():
        spine.set_color("white")

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PDF REPORT
# =====================================================

def create_pdf(load, temp, rpm, oil, result):

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(file.name)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "THERMOLYTIX REPORT",
            styles['Title']
        )
    )

    content.append(
        Paragraph(f"Load: {load}", styles['Normal'])
    )

    content.append(
        Paragraph(f"Ambient Temp: {temp}", styles['Normal'])
    )

    content.append(
        Paragraph(f"RPM: {rpm}", styles['Normal'])
    )

    content.append(
        Paragraph(f"Oil Condition: {oil}", styles['Normal'])
    )

    content.append(
        Paragraph(
            f"Predicted Temperature: {result:.2f} °C",
            styles['Normal']
        )
    )

    doc.build(content)

    return file.name

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button("📁 Download PDF Report"):

    pdf = create_pdf(
        load,
        temp,
        rpm,
        oil,
        pred_value
    )

    with open(pdf, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="thermolytix_report.pdf"
        )
