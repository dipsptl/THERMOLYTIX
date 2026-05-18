import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
import tempfile
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="THERMOLYTIX AI Dashboard", layout="wide")

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg   = get_base64("bg.jpg")
logo = get_base64("logo.png")

st.markdown(f"""
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding: 0.2rem 0.7rem 0.2rem 0.7rem !important;
    max-width: 100% !important;
}}

header {{ display:none !important; }}
#MainMenu {{ display:none !important; }}
footer {{ display:none !important; }}
[data-testid="stToolbar"] {{ display:none !important; }}
[data-testid="stDecoration"] {{ display:none !important; }}

.logo-img {{ width:190px; display:block; }}

.status-pill {{
    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 5px 14px;
    color: white; font-size:12px; font-weight:600;
    display:inline-flex; align-items:center; gap:6px;
    float:right; margin-top:6px;
}}

.card {{
    background: rgba(0,0,0,0.75);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 12px;
    padding: 9px 12px;
    backdrop-filter: blur(6px);
    margin-bottom: 5px;
}}

.sec-title {{
    color:#ff8800; font-size:12px; font-weight:700;
    margin-bottom:5px; display:flex; align-items:center; gap:5px;
}}

.dash-h {{ color:white; font-size:17px; font-weight:800; margin-bottom:2px; }}
.dash-p {{ color:#aaa; font-size:10px; }}

[data-testid="stSlider"] {{ padding:0 !important; }}
[data-testid="stSlider"] > div {{ padding:0 !important; }}
[data-testid="stSlider"] label {{ display:none !important; }}
[data-testid="stSlider"] [data-baseweb="slider"] {{ margin:1px 0 !important; }}

.si {{ font-size:14px; padding-top:11px; text-align:center; }}
.sl {{ color:#ccc; font-size:11px; padding-top:13px; }}
.sv {{ display:flex; align-items:center; gap:3px; padding-top:9px; }}
.sb {{
    background:rgba(255,255,255,0.07);
    border:1px solid rgba(255,255,255,0.15);
    border-radius:5px; color:white; font-size:12px; font-weight:700;
    min-width:46px; text-align:center; padding:2px 4px;
}}
.su {{ color:#777; font-size:10px; }}

.stButton > button {{
    width:100%;
    background: linear-gradient(90deg,#ff8800,#00cfff);
    color:white; border:none; border-radius:8px;
    font-size:13px; font-weight:800; height:36px; letter-spacing:1px;
}}

.temp-num {{
    font-size:50px; font-weight:900; color:white;
    line-height:1; margin:3px 0;
    font-family:'Arial Black',sans-serif;
}}
.temp-deg {{ font-size:20px; color:#bbb; }}

.safe-box {{
    background:#004d1a; border-radius:7px;
    padding:5px 12px; color:#55ff88;
    font-size:13px; font-weight:700;
    margin:4px 0; display:flex; align-items:center; gap:7px;
}}

.warn-box {{
    background:rgba(70,50,0,0.7);
    border:1px solid rgba(180,140,0,0.25);
    border-radius:7px; padding:5px 9px;
    margin-bottom:4px; color:#e0c060;
    font-size:11px; display:flex; align-items:center; gap:6px;
}}

.graph-card {{
    background:rgba(0,0,0,0.75);
    border:1px solid rgba(255,140,0,0.35);
    border-radius:10px; padding:4px 6px;
}}
</style>
""", unsafe_allow_html=True)

# ── ROW 1: LOGO + STATUS ──
r1, r2 = st.columns([5, 1], gap="small")
with r1:
    st.markdown(f'<img class="logo-img" src="data:image/png;base64,{logo}">', unsafe_allow_html=True)
with r2:
    st.markdown('<div class="status-pill">🟢 System Operational</div>', unsafe_allow_html=True)

# ── DATA & MODEL ──
data  = pd.read_csv("cooling_data.csv")
X     = data[['Load','Ambient_Temp','RPM','Oil_Condition']]
y     = data['Temperature']
model = LinearRegression()
model.fit(X, y)

# ── ROW 2: LEFT + RIGHT ──
left, right = st.columns([1.05, 1], gap="small")

with left:

    # AI Dashboard card
    st.markdown("""
    <div class="card">
        <div class="dash-h">AI Dashboard</div>
        <div class="dash-p">Enter parameters to get AI-powered temperature predictions and system insights.</div>
    </div>
    """, unsafe_allow_html=True)

    # Enter Parameters card
    st.markdown('<div class="card"><div class="sec-title">⚙️ Enter Parameters</div>', unsafe_allow_html=True)

    cfg = [
        ("🏎️", "Load",          "load", 50,   100,  70,   "%"),
        ("🌡️", "Ambient Temp",  "temp", 25,   50,   30,   "°C"),
        ("⚡",  "RPM",           "rpm",  1200, 1800, 1450, "RPM"),
        ("🛢️", "Oil Condition", "oil",  40,   100,  75,   "%"),
    ]
    vals = {}
    for icon, label, key, mn, mx, df, unit in cfg:
        c1, c2, c3, c4 = st.columns([0.07, 0.17, 0.53, 0.23], gap="small")
        with c1: st.markdown(f'<div class="si">{icon}</div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="sl">{label}</div>', unsafe_allow_html=True)
        with c3: v = st.slider(label, mn, mx, df, key=key, label_visibility="collapsed")
        vals[key] = v
        with c4: st.markdown(f'<div class="sv"><div class="sb">{v}</div><div class="su">{unit}</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.button("PREDICT TEMPERATURE →", use_container_width=True)

with right:

    load = vals["load"]
    temp = vals["temp"]
    rpm  = vals["rpm"]
    oil  = vals["oil"]

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    # Prediction Summary card
    st.markdown(f"""
    <div class="card">
        <div class="sec-title">📊 Prediction Summary</div>
        <div class="temp-num">{pred_value:.1f} <span class="temp-deg">°C</span></div>
        <div class="safe-box">🟢 Safe</div>
    </div>
    """, unsafe_allow_html=True)

    # Suggestions card
    s = ""
    if rpm  > 1400: s += '<div class="warn-box">⚠️ Reduce RPM to control heat</div>'
    if oil  <   80: s += '<div class="warn-box">⚠️ Oil condition poor – maintenance needed</div>'
    if load >   65: s += '<div class="warn-box">⚠️ High load – reduce load</div>'
    if temp >   28: s += '<div class="warn-box">⚠️ High ambient temp – improve cooling</div>'
    if s:
        st.markdown(f'<div class="card"><div class="sec-title">💡 Suggestions</div>{s}</div>', unsafe_allow_html=True)

# ── ROW 3: ANALYSIS ──
st.markdown('<div style="color:#ff8800;font-size:12px;font-weight:700;margin:3px 0 4px 0;">📈 Analysis</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2, gap="small")

def chart(xd, yd, title, xl, yl):
    fig, ax = plt.subplots(figsize=(4, 1.8))
    ax.scatter(xd, yd, s=28, color='#00bfff', alpha=0.75)
    ax.set_facecolor("#050b18")
    fig.patch.set_facecolor("#050b18")
    ax.set_title(title, color="white", fontsize=9, fontweight='bold', pad=3)
    ax.set_xlabel(xl, color="white", fontsize=8)
    ax.set_ylabel(yl, color="white", fontsize=8)
    ax.tick_params(colors='white', labelsize=7)
    for sp in ax.spines.values():
        sp.set_color("white")
        sp.set_linewidth(0.4)
    ax.grid(True, alpha=0.08, color='white', linewidth=0.4)
    fig.tight_layout(pad=0.4)
    return fig

with g1:
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(chart(data['Load'], data['Temperature'], "Temperature vs Load", "Load (%)", "Temperature (°C)"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(chart(data['RPM'], data['Temperature'], "Temperature vs RPM", "RPM", "Temperature (°C)"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 4: PDF DOWNLOAD ──
def create_pdf(load, temp, rpm, oil, result):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc  = SimpleDocTemplate(file.name)
    styles = getSampleStyleSheet()
    content = [
        Paragraph("THERMOLYTIX REPORT", styles['Title']),
        Paragraph(f"Load: {load}", styles['Normal']),
        Paragraph(f"Ambient Temp: {temp}", styles['Normal']),
        Paragraph(f"RPM: {rpm}", styles['Normal']),
        Paragraph(f"Oil Condition: {oil}", styles['Normal']),
        Paragraph(f"Predicted Temperature: {result:.2f} °C", styles['Normal']),
    ]
    doc.build(content)
    return file.name

if st.button("📁 Download PDF Report", use_container_width=False):
    pdf = create_pdf(load, temp, rpm, oil, pred_value)
    with open(pdf, "rb") as f:
        st.download_button("⬇ Download Report", f, file_name="thermolytix_report.pdf")
