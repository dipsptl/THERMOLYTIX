import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Thermolytix AI",
    layout="wide"
)

# =========================================
# LOAD LOGO
# =========================================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64("logo.png")

# =========================================
# BACKGROUND
# =========================================
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
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }}

        section[data-testid="stSidebar"] {{
            display:none;
        }}

        </style>
        """, unsafe_allow_html=True)

    except:
        pass

set_bg()

# =========================================
# HEADER
# =========================================
st.markdown(f"""
<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:20px;
">

<div style="display:flex; align-items:center; gap:15px;">

<img src="data:image/png;base64,{logo}" width="120">

<div>
<div style="
font-size:42px;
font-weight:900;
color:#FF8C00;
line-height:1;
">
THERMO<span style="color:#29D8FF;">LYTIX</span>
</div>

<div style="
font-size:14px;
color:#DDDDDD;
letter-spacing:2px;
margin-top:5px;
">
GEARBOX THERMAL ANALYTICS
</div>
</div>

</div>

<div style="
display:flex;
gap:15px;
">

<div style="
background:rgba(0,0,0,0.5);
padding:12px 18px;
border-radius:12px;
border:1px solid rgba(255,140,0,0.25);
color:#00FF88;
font-weight:600;
">
🟢 System Operational
</div>

</div>

</div>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =========================================
# MAIN DASHBOARD
# =========================================
st.markdown("""
<div style="
background:rgba(0,0,0,0.45);
border-radius:25px;
padding:30px;
border:1px solid rgba(255,140,0,0.18);
backdrop-filter:blur(8px);
">
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

# =========================================
# LEFT SIDE
# =========================================
with left:

    st.markdown("""
    <div style="
    font-size:46px;
    font-weight:800;
    color:#FF8C00;
    margin-bottom:10px;
    ">
    ⚙️ Cooling Tower Gear Temp.
    </div>

    <div style="
    font-size:24px;
    color:white;
    font-weight:600;
    margin-bottom:18px;
    ">
    AI Dashboard
    </div>

    <div style="
    color:#CCCCCC;
    margin-bottom:30px;
    font-size:16px;
    ">
    Enter parameters to get AI-powered temperature predictions and system insights.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:rgba(0,0,0,0.35);
    border-radius:20px;
    padding:25px;
    border:1px solid rgba(255,140,0,0.18);
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    color:#FF9C1A;
    font-size:28px;
    font-weight:700;
    margin-bottom:20px;
    ">
    ⚙️ Enter Parameters
    </div>
    """, unsafe_allow_html=True)

    load = st.slider("Load (%)", 50, 100, 70)

    temp = st.slider("Ambient Temp (°C)", 25, 50, 30)

    rpm = st.slider("RPM", 1200, 1800, 1450)

    oil = st.slider("Oil Condition (%)", 40, 100, 75)

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.button("PREDICT TEMPERATURE", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# RIGHT SIDE
# =========================================
with right:

    st.markdown("""
    <div style="
    background:rgba(0,0,0,0.35);
    border-radius:20px;
    padding:25px;
    border:1px solid rgba(255,140,0,0.18);
    margin-top:90px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    color:#FF9C1A;
    font-size:28px;
    font-weight:700;
    margin-bottom:18px;
    ">
    📊 Prediction Summary
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
    color:white;
    font-size:64px;
    font-weight:900;
    ">
    {pred_value:.1f}
    <span style="font-size:26px;">°C</span>
    </div>
    """, unsafe_allow_html=True)

    if pred_value > 90:
        st.error("🔴 Danger")

    elif pred_value > 80:
        st.warning("🟠 Warning")

    else:
        st.success("🟢 Safe")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
    color:#FF9C1A;
    font-size:26px;
    font-weight:700;
    margin-bottom:15px;
    ">
    💡 Suggestions
    </div>
    """, unsafe_allow_html=True)

    if rpm > 1500:
        st.warning("Reduce RPM to control heat")

    if oil < 60:
        st.warning("Oil condition poor – maintenance needed")

    if load > 75:
        st.warning("High load – reduce load")

    if temp > 35:
        st.warning("High ambient temp – improve cooling")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# ANALYSIS SECTION
# =========================================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
background:rgba(0,0,0,0.35);
border-radius:20px;
padding:25px;
border:1px solid rgba(255,140,0,0.18);
">
""", unsafe_allow_html=True)

st.markdown("""
<div style="
color:#FF9C1A;
font-size:30px;
font-weight:700;
margin-bottom:20px;
">
📈 Analysis
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.scatter(data['Load'], data['Temperature'])
    ax1.set_xlabel("Load (%)")
    ax1.set_ylabel("Temperature (°C)")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.scatter(data['RPM'], data['Temperature'])
    ax2.set_xlabel("RPM")
    ax2.set_ylabel("Temperature (°C)")
    st.pyplot(fig2)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# PDF FUNCTION
# =========================================
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

# =========================================
# DOWNLOAD REPORT
# =========================================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("📁 Download PDF Report"):

    pdf_file = create_pdf(load, temp, rpm, oil, pred_value)

    with open(pdf_file, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="Cooling_Tower_Report.pdf"
        )

st.markdown("</div>", unsafe_allow_html=True)
