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

* {{
    margin: 0;
    padding: 0;
}}

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 0.2rem !important;
    padding-left: 0.6rem !important;
    padding-right: 0.6rem !important;
    max-width: 100% !important;
}}

header {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}

/* LOGO */
.logo-wrap {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 2px 0;
}}
.logo-img {{ width: 90px; }}
.logo-title {{
    color: #ff8800;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 1px;
    line-height: 1.1;
    font-family: 'Arial Black', sans-serif;
}}
.logo-sub {{
    color: #ffffff;
    font-size: 06px;
    font-weight: 500;
    letter-spacing: 2px;
    margin-top: 1px;
}}

/* STATUS */
.system-box {{
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 06px;
    padding: 4px 10px;
    color: white;
    font-size: 08px;
    font-weight: 400;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    float: right;
    margin-top: 6px;
}}

/* CARDS */
.main-card {{
    background: rgba(0,0,0,0.62);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 08px;
    padding: 10px 08px;
    backdrop-filter: blur(4px);
    margin-bottom: 5px;
}}

.title-orange {{
    color: #ff8800;
    font-size: 08px;
    font-weight: 500;
    margin-bottom: 4px;
}}

/* BIG TEMP NUMBER */
.big-number {{
    font-size: 52px;
    font-weight: 900;
    color: white;
    margin: 4px 0;
    line-height: 1;
    font-family: 'Arial Black', sans-serif;
}}
.deg-small {{
    font-size: 22px;
    color: #cccccc;
    font-weight: 400;
}}

/* SAFE BOX */
.safe-box {{
    background: #005520;
    border-radius: 8px;
    padding: 6px 12px;
    color: #67ff99;
    font-size: 14px;
    font-weight: 700;
    margin: 6px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* WARN BOX */
.warn-box {{
    background: rgba(80,60,0,0.6);
    border: 1px solid rgba(200,160,0,0.25);
    border-radius: 8px;
    padding: 6px 10px;
    margin-bottom: 5px;
    color: #e8d080;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

/* PREDICT BUTTON */
.stButton > button {{
    width: 100%;
    background: linear-gradient(90deg, #ff8800, #00cfff);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 800;
    height: 40px;
    letter-spacing: 1px;
}}

/* SLIDERS */
[data-testid="stSlider"] {{ padding: 0 !important; }}
[data-testid="stSlider"] > div {{ padding: 0 !important; }}
[data-testid="stSlider"] label {{ display: none !important; }}
.stSlider {{ margin-bottom: 0 !important; }}

.slider-label {{
    font-size: 11px;
    color: #cccccc;
    margin-bottom: 1px;
    margin-top: 4px;
}}

/* VALUE BADGE */
.val-badge {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 5px;
    color: white;
    font-size: 12px;
    font-weight: 700;
    min-width: 50px;
    text-align: center;
    padding: 3px 5px;
}}
.val-unit {{
    color: #888;
    font-size: 10px;
    min-width: 26px;
}}
.row-icon {{
    font-size: 15px;
    padding-top: 12px;
    text-align: center;
    min-width: 18px;
}}
.row-label {{
    color: #cccccc;
    font-size: 11px;
    padding-top: 14px;
    min-width: 80px;
}}
.row-val {{
    display: flex;
    align-items: center;
    gap: 4px;
    padding-top: 10px;
}}

/* GRAPH */
.graph-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 12px;
    padding: 6px 8px;
}}

[data-testid="stMetricValue"] {{
    font-size: 24px !important;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

top1, top2 = st.columns([5, 1], gap="small")

with top1:
    st.markdown(f"""
    <div class="logo-wrap">
        <img class="logo-img" src="data:image/png;base64,{logo}">
        <div>
            <div class="logo-title">THERMOLYTIX</div>
            <div class="logo-sub">GEARBOX THERMAL ANALYTICS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="system-box">🟢 System Operational</div>
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

left, right = st.columns([1.05, 1], gap="small")

# =====================================================
# LEFT SIDE
# =====================================================

with left:

    # Dashboard title card
    st.markdown("""
    <div class="main-card">
        <h2 style="color:white; font-size:18px; margin:0 0 3px 0;">AI Dashboard</h2>
        <p style="color:#aaa; font-size:11px; margin:0;">Enter parameters to get AI-powered temperature predictions and system insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Parameters card with sliders
    st.markdown('<div class="main-card"><div class="title-orange">⚙️ Enter Parameters</div>', unsafe_allow_html=True)

    slider_cfg = [
        ("🏎️", "Load",          "load", 50,   100,  70,   "%"),
        ("🌡️", "Ambient Temp",  "temp", 25,   50,   30,   "°C"),
        ("⚡",  "RPM",           "rpm",  1200, 1800, 1450, "RPM"),
        ("🛢️", "Oil Condition", "oil",  40,   100,  75,   "%"),
    ]

    vals = {}
    for icon, label, key, mn, mx, df, unit in slider_cfg:
        c1, c2, c3, c4 = st.columns([0.07, 0.18, 0.52, 0.23], gap="small")
        with c1:
            st.markdown(f'<div class="row-icon">{icon}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="row-label">{label}</div>', unsafe_allow_html=True)
        with c3:
            v = st.slider(label, mn, mx, df, key=key, label_visibility="collapsed")
            vals[key] = v
        with c4:
            st.markdown(
                f'<div class="row-val">'
                f'<div class="val-badge">{v}</div>'
                f'<div class="val-unit">{unit}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.button("PREDICT TEMPERATURE →", use_container_width=True)

# =====================================================
# RIGHT SIDE
# =====================================================

with right:

    load = vals["load"]
    temp = vals["temp"]
    rpm  = vals["rpm"]
    oil  = vals["oil"]

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <div class="main-card">
        <div class="title-orange">📊 Prediction Summary</div>
        <div class="big-number">{pred_value:.1f} <span class="deg-small">°C</span></div>
        <div class="safe-box">🟢 &nbsp;Safe</div>
    </div>
    """, unsafe_allow_html=True)

    suggestions_html = ""
    if rpm  > 1400: suggestions_html += '<div class="warn-box">⚠️ Reduce RPM to control heat</div>'
    if oil  <   80: suggestions_html += '<div class="warn-box">⚠️ Oil condition poor – maintenance needed</div>'
    if load >   65: suggestions_html += '<div class="warn-box">⚠️ High load – reduce load</div>'
    if temp >   28: suggestions_html += '<div class="warn-box">⚠️ High ambient temp – improve cooling</div>'

    if suggestions_html:
        st.markdown(f"""
        <div class="main-card">
            <div class="title-orange">💡 Suggestions</div>
            {suggestions_html}
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# ANALYSIS SECTION
# =====================================================

st.markdown("""
<div style="color:#ff8800; font-size:13px; font-weight:700; margin: 4px 0 5px 0;">📈 Analysis</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2, gap="small")

def make_chart(xdata, ydata, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(4, 2.0))
    ax.scatter(xdata, ydata, s=30, color='#00bfff', alpha=0.75)
    ax.set_facecolor("#050b18")
    fig.patch.set_facecolor("#050b18")
    ax.set_title(title, color="white", fontsize=10, fontweight='bold', pad=4)
    ax.set_xlabel(xlabel, color="white", fontsize=9)
    ax.set_ylabel(ylabel, color="white", fontsize=9)
    ax.tick_params(colors='white', labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(0.5)
    ax.grid(True, alpha=0.1, color='white', linewidth=0.5)
    fig.tight_layout(pad=0.5)
    return fig

with g1:
    fig1 = make_chart(data['Load'], data['Temperature'],
                      "Temperature vs Load", "Load (%)", "Temperature (°C)")
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    fig2 = make_chart(data['RPM'], data['Temperature'],
                      "Temperature vs RPM", "RPM", "Temperature (°C)")
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PDF REPORT
# =====================================================

def create_pdf(load, temp, rpm, oil, result):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc  = SimpleDocTemplate(file.name)
    styles  = getSampleStyleSheet()
    content = [
        Paragraph("THERMOLYTIX REPORT",                      styles['Title']),
        Paragraph(f"Load: {load}",                           styles['Normal']),
        Paragraph(f"Ambient Temp: {temp}",                   styles['Normal']),
        Paragraph(f"RPM: {rpm}",                             styles['Normal']),
        Paragraph(f"Oil Condition: {oil}",                   styles['Normal']),
        Paragraph(f"Predicted Temperature: {result:.2f} °C", styles['Normal']),
    ]
    doc.build(content)
    return file.name

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

if st.button("📁 Download PDF Report", use_container_width=True):
    pdf = create_pdf(load, temp, rpm, oil, pred_value)
    with open(pdf, "rb") as f:
        st.download_button(
            "⬇ Download Report",
            f,
            file_name="thermolytix_report.pdf",
            use_container_width=True
        )
