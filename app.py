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
    page_title="Thermolytix AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# BACKGROUND IMAGE
# =====================================================

def add_bg():

    with open("bg.jpg", "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    header {{
        visibility: hidden;
    }}

    .block-container {{
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }}

    /* REMOVE WHITE */
    .stAppViewContainer {{
        background: transparent;
    }}

    /* GLASS CARD */
    .glass {{
        background: rgba(0,0,0,0.45);
        border: 1px solid rgba(255,140,0,0.25);
        border-radius: 18px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(0,0,0,0.4);
    }}

    .title {{
        color: #ff8c00;
        font-size: 36px;
        font-weight: 700;
    }}

    .sub {{
        color: white;
        font-size: 18px;
    }}

    .section {{
        color: #ff8c00;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .metric {{
        color: white;
        font-size: 52px;
        font-weight: bold;
    }}

    .safe {{
        background: rgba(0,255,120,0.18);
        color: #65ff9c;
        padding: 12px;
        border-radius: 10px;
        font-size: 20px;
        text-align: center;
    }}

    .warn {{
        background: rgba(255,0,0,0.18);
        color: #ff6565;
        padding: 12px;
        border-radius: 10px;
        font-size: 20px;
        text-align: center;
    }}

    .suggest {{
        background: rgba(255,165,0,0.15);
        color: #ffd580;
        padding: 12px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 16px;
    }}

    .stSlider label {{
        color: white !important;
    }}

    .stButton>button {{
        width: 100%;
        background: linear-gradient(90deg,#ff8c00,#00c2ff);
        color: white;
        border: none;
        border-radius: 12px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }}

    .stDownloadButton>button {{
        width: 100%;
        background: linear-gradient(90deg,#1f1f1f,#303030);
        color: white;
        border-radius: 12px;
        border: 1px solid #555;
        height: 50px;
        font-size: 18px;
    }}

    div[data-testid="stVerticalBlock"] > div:has(.element-container) {{
        gap: 0.7rem;
    }}

    </style>
    """, unsafe_allow_html=True)

add_bg()

# =====================================================
# LOGO
# =====================================================

st.image("logo.png", width=340)

# =====================================================
# LOAD DATA
# =====================================================

data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns([1, 3])

# =====================================================
# LEFT PANEL
# =====================================================

with left:

    st.markdown("""
    <div class="glass">
        <div class="sub" style="font-size:34px;font-weight:700;">
            AI Dashboard
        </div>

        <div style="color:#cfcfcf;margin-top:10px;">
            Enter parameters to get AI powered temperature
            prediction and system insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="section">⚙️ Enter Parameters</div>
    """, unsafe_allow_html=True)

    load = st.slider("Load", 50, 100, 50)
    temp = st.slider("Ambient Temp", 25, 50, 25)
    rpm = st.slider("RPM", 1200, 1800, 1200)
    oil = st.slider("Oil Condition", 40, 100, 40)

    st.button("PREDICT TEMPERATURE")

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PREDICTION
# =====================================================

pred_value = model.predict([[load, temp, rpm, oil]])[0]

# =====================================================
# RIGHT PANEL
# =====================================================

with right:

    top1, top2 = st.columns([1.4, 1])

    # =========================================
    # PREDICTION SUMMARY
    # =========================================

    with top1:

        st.markdown(f"""
        <div class="glass" style="height:250px;">
            <div class="section">📊 Prediction Summary</div>

            <div class="metric">
                {pred_value:.1f}<span style="font-size:22px;"> °C</span>
            </div>
        """, unsafe_allow_html=True)

        if pred_value > 90:
            st.markdown("""
            <div class="warn">🔴 Danger</div>
            """, unsafe_allow_html=True)

        elif pred_value > 80:
            st.markdown("""
            <div class="warn">🟠 Warning</div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="safe">🟢 Safe</div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================
    # SUGGESTIONS
    # =========================================

    with top2:

        suggestion = "System Running Normally"

        if oil < 60:
            suggestion = "Oil condition poor – maintenance needed"

        elif rpm > 1500:
            suggestion = "Reduce RPM to control heat"

        elif load > 75:
            suggestion = "High load detected"

        elif temp > 35:
            suggestion = "Improve cooling system"

        st.markdown(f"""
        <div class="glass" style="height:250px;">
            <div class="section">💡 Suggestions</div>

            <div class="suggest" style="margin-top:60px;">
                {suggestion}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================================
    # ANALYSIS
    # =========================================

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="section">📈 Analysis</div>
    """, unsafe_allow_html=True)

    g1, g2 = st.columns(2)

    # =========================================
    # GRAPH 1
    # =========================================

    with g1:

        fig1, ax1 = plt.subplots(figsize=(6,4))

        ax1.scatter(
            data['Load'],
            data['Temperature']
        )

        ax1.set_facecolor("#050b16")

        fig1.patch.set_facecolor("#050b16")

        ax1.set_xlabel("Load (%)", color="white")
        ax1.set_ylabel("Temperature (°C)", color="white")

        ax1.tick_params(colors='white')

        for spine in ax1.spines.values():
            spine.set_color('#666')

        st.pyplot(fig1, use_container_width=True)

    # =========================================
    # GRAPH 2
    # =========================================

    with g2:

        fig2, ax2 = plt.subplots(figsize=(6,4))

        ax2.scatter(
            data['RPM'],
            data['Temperature']
        )

        ax2.set_facecolor("#050b16")

        fig2.patch.set_facecolor("#050b16")

        ax2.set_xlabel("RPM", color="white")
        ax2.set_ylabel("Temperature (°C)", color="white")

        ax2.tick_params(colors='white')

        for spine in ax2.spines.values():
            spine.set_color('#666')

        st.pyplot(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PDF REPORT
# =====================================================

def create_pdf(load, temp, rpm, oil, result):

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(file.name)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Thermolytix AI Report", styles['Title'])
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
        Paragraph(f"Predicted Temperature: {result:.2f} °C", styles['Normal'])
    )

    doc.build(content)

    return file.name

# =====================================================
# DOWNLOAD
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

pdf_file = create_pdf(load, temp, rpm, oil, pred_value)

with open(pdf_file, "rb") as f:

    st.download_button(
        "📁 Download PDF Report",
        f,
        file_name="Thermolytix_Report.pdf"
    )
