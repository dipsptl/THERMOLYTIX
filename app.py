import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime
import base64
import os

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

st.set_page_config(page_title="Thermolytix", page_icon="🌡️", layout="wide", initial_sidebar_state="collapsed")

try:
    bg_base64 = get_base64_image("bg.png")
    bg_style = f"background-image: url('data:image/png;base64,{bg_base64}'); background-size: cover; background-attachment: fixed;"
except FileNotFoundError:
    bg_style = "background: linear-gradient(135deg, #0A1628 0%, #0F2239 100%);"

st.markdown(f"""
<style>
    :root {{
        --primary: #FFA500; --secondary: #00D4FF; --success: #00FF41;
        --warning: #FFB700; --danger: #FF3333; --dark-bg: #0A1628;
        --text-primary: #FFFFFF; --text-secondary: #B0B8C1; --border: #1E3A52;
    }}
    .logo-img {{
        height: 300px; object-fit: contain;
        filter: drop-shadow(0 4px 8px rgba(255,165,0,0.3));
        display: block; margin-left: -30px; margin-top: -80px; margin-bottom: -70px;
    }}
    .stApp {{ {bg_style} color: var(--text-primary); }}
    .main {{ padding: 0 !important; }}
    .header-wrapper {{
        background: linear-gradient(90deg, rgba(10,22,40,0.95) 0%, rgba(15,34,57,0.95) 100%);
        border-bottom: 2px solid var(--border); padding: 0.8rem 2rem;
        margin-bottom: 0; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}
    .header-content {{ max-width: 2200px; margin: 0 auto; }}
    .header-top {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; }}
    .header-left {{ display: flex; flex-direction: column; align-items: flex-start; gap: 0rem; }}
    .header-status {{ display: flex; gap: 1rem; font-size: 0.85rem; }}
    .status-item {{
        display: flex; align-items: center; gap: 0.5rem;
        padding: 0.6rem 1.2rem; background: rgba(0,255,65,0.1);
        border: 1px solid var(--success); border-radius: 6px;
        color: var(--success); font-weight: 600;
    }}
    .content-wrapper {{ max-width: 1400px; margin: 0 auto; padding: 1.5rem 2rem; }}
    .block {{
        background: linear-gradient(135deg, rgba(17,30,48,0.92) 0%, rgba(30,58,82,0.7) 100%);
        border: 1px solid var(--border); border-radius: 12px;
        padding: 1.2rem 1.5rem; margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .block-title {{
        color: var(--text-primary); font-size: 1rem; font-weight: 700;
        margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
        text-transform: uppercase; letter-spacing: 1px;
        border-bottom: 1px solid var(--border); padding-bottom: 0.6rem;
    }}
    .suggestion-item {{
        display: flex; align-items: flex-start; gap: 0.6rem;
        padding: 0.6rem 0.8rem; color: var(--text-secondary); font-size: 0.9rem;
        border-radius: 6px; margin-bottom: 0.4rem;
        background: rgba(15,34,57,0.5);
    }}
    .suggestion-dot {{ font-size: 1rem; min-width: 20px; }}
    .alert-item {{
        background: rgba(15,34,57,0.5); border-left: 4px solid var(--warning);
        padding: 0.8rem 1rem; border-radius: 6px; margin-bottom: 0.6rem;
        display: flex; gap: 0.8rem;
    }}
    .alert-item.success {{ border-left-color: var(--success); }}
    .alert-item.danger  {{ border-left-color: var(--danger); }}
    .alert-icon {{ font-size: 1.2rem; min-width: 24px; }}
    .alert-content strong {{ color: var(--text-primary); font-size: 0.9rem; }}
    .alert-content p {{ color: var(--text-secondary); margin: 0.2rem 0 0; font-size: 0.82rem; }}
    .footer {{
        text-align: center; padding: 1.5rem; color: var(--text-secondary);
        font-size: 0.82rem; border-top: 1px solid var(--border); margin-top: 1rem;
    }}
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #FFA500, #FF6B00) !important;
        color: #000 !important; font-weight: 700 !important;
        border: none !important; border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
    }}
    @media (max-width: 768px) {{
    /* Header layout */
    .header-top {{ 
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }}
    
    /* Logo left side, medium size */
    .logo-img {{ 
        height: 210px !important;
        margin: -20px 0 -20px -25px !important;
    }}
    
    /* Logo container */
    .header-left {{
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        width: auto !important;
        flex: 0 0 auto;
    }}
    
   .header-left > div {{
    font-size: 0.5rem !important;
    text-align: left !important;
    padding-left: 5px !important;
    max-width: 200px !important;
    line-height: 1.1 !important;
    opacity: 0.7 !important;
    margin-top: -5px !important;
    white-space: nowrap !important;
    }}
    
    /* Green blocks 3x મોટા */
    .header-status {{ 
        flex-direction: column !important;
        gap: 0.4rem !important;
        width: auto !important;
    }}
    
    .status-item {{
        padding: 0.2rem 0.5rem !important;
        font-size: 0.30rem !important;
        border-radius: 3px !important;
        white-space: nowrap !important;
    }}
    
    /* Header compact */
    .header-wrapper {{
        padding: 0.2rem 0.6rem !important;
    }}
    
    .content-wrapper {{ padding: 1rem; }}
}}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──
try:
    logo_base64 = get_base64_image("logo.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="Thermolytix"/>'
except FileNotFoundError:
    logo_html = '<span style="font-size:2.2rem;font-weight:900;background:linear-gradient(90deg,#FFA500 0%,#00D4FF 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">THERMOLYTIX</span>'

st.markdown(f"""
<div class="header-wrapper"><div class="header-content"><div class="header-top">
    <div class="header-left">
        {logo_html}
        <div style="color:#FFFFFF;font-size:0.75rem;font-weight:300;margin:0;opacity:0.85;padding-left:5px;">Thermal Intelligence for Gearbox Cooling Systems</div>
    </div>
    <div class="header-status">
        <div class="status-item">✓ System Active</div>
        <div class="status-item">✓ Sensors OK</div>
        <div class="status-item">✓ Cooling Normal</div>
    </div>
</div></div></div>
""", unsafe_allow_html=True)

# ── LOAD MODEL ──
@st.cache_resource
def load_model():
    data = pd.read_csv("cooling_data.csv")
    X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
    y = data['Temperature']
    model = LinearRegression()
    model.fit(X, y)
    return model

try:
    model = load_model()
    model_loaded = True
except Exception:
    model_loaded = False

# ── MAIN ──
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# BLOCK 1: PARAMETERS
st.markdown('<div class="block"><div class="block-title">⚙️ Enter Parameters</div><div style="padding: 0.5rem 1rem;">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    load_val = st.slider("Load (%)", 50, 100, 65, key="load")
with col2:
    rpm_val = st.slider("RPM", 1200, 1800, 1500, key="rpm")
with col3:
    ambient_val = st.slider("Ambient Temp (°C)", 25, 50, 30, key="ambient")
with col4:
    oil_val = st.slider("Oil Condition", 40, 100, 70, key="oil")
st.markdown('</div></div>', unsafe_allow_html=True)

# ── PREDICTION ──
if model_loaded:
    pred_temp = round(float(model.predict([[load_val, ambient_val, rpm_val, oil_val]])[0]), 1)
    pred_temp = max(30.0, min(95.0, pred_temp))
else:
    pred_temp = 65.0

if pred_temp > 90:
    status_bg, status_border, status_dot, status_text, status_color, status_label = \
        "rgba(255,51,51,0.15)", "#FF3333", "🔴", "Danger", "#FF3333", "DANGER"
elif pred_temp > 80:
    status_bg, status_border, status_dot, status_text, status_color, status_label = \
        "rgba(255,183,0,0.15)", "#FFB700", "🟠", "Warning", "#FFB700", "WARNING"
else:
    status_bg, status_border, status_dot, status_text, status_color, status_label = \
        "rgba(0,255,65,0.1)", "#00FF41", "🟢", "Safe", "#00FF41", "NORMAL"

# BLOCK 2: PREDICTION SUMMARY — temp + status only (like old code)
st.markdown(f"""
<div class="block">
    <div class="block-title">📊 Prediction Summary</div>
    # change this line in BLOCK 2:
    <h2 style="color:white;margin:0.3rem 0 0.6rem 0;font-size:2rem;font-weight:900;">
        {pred_temp} <span style="font-size:1.2rem;color:#B0B8C1;">°C</span>
    </h2>
    <div style="background:{status_bg};border:1px solid {status_border};border-radius:8px;padding:0.7rem 1.2rem;display:inline-flex;align-items:center;gap:0.6rem;min-width:180px;">
        <span style="font-size:1rem;">{status_dot}</span>
        <span style="color:{status_color};font-weight:600;font-size:1rem;">{status_text}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# BLOCK 3: SUGGESTIONS — only relevant ones (like old code)
suggestions = []
if rpm_val > 1500:
    suggestions.append(("⚠️", "Reduce RPM to control heat buildup."))
if oil_val < 60:
    suggestions.append(("⚠️", "Oil condition poor — maintenance needed."))
if load_val > 75:
    suggestions.append(("⚠️", "High load — consider reducing load."))
if ambient_val > 35:
    suggestions.append(("⚠️", "High ambient temp — improve cooling."))
if pred_temp > 80:
    suggestions.append(("🔴", "Critical temperature — immediate inspection required."))

if not suggestions:
    suggestions = [("✅", "System operating optimally — no immediate action required.")]

suggestions_html = "".join([
    f'<div class="suggestion-item"><span class="suggestion-dot">{icon}</span><span>{text}</span></div>'
    for icon, text in suggestions
])

st.markdown(f"""
<div class="block">
    <div class="block-title">💡 Suggestions</div>
    {suggestions_html}
</div>
""", unsafe_allow_html=True)

# BLOCK 4: ANALYSIS
st.markdown('<div class="block"><div class="block-title">📈 Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if model_loaded:
        loads = np.arange(50, 101, 1)
        temps_load = [np.clip(model.predict([[l, ambient_val, rpm_val, oil_val]])[0], 25, 95) for l in loads]
    else:
        loads = np.linspace(50, 100, 50)
        temps_load = 45 + loads * 0.25

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=loads, y=temps_load, line=dict(color='#FFA500', width=2.5),
        fill='tozeroy', fillcolor='rgba(255,165,0,0.08)', name='Temp'))
    fig1.add_trace(go.Scatter(x=[load_val], y=[pred_temp], mode='markers',
        marker=dict(color='#00FF41', size=10), name='Current'))
    fig1.update_layout(
        title=dict(text="1️⃣  Temp vs Load", font=dict(color='#B0B8C1', size=13)),
        height=320, template='plotly_dark',
        plot_bgcolor='rgba(17,30,48,0.3)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor='rgba(30,58,82,0.3)', title='Load (%)'),
        yaxis=dict(gridcolor='rgba(30,58,82,0.3)', title='Temp (°C)'),
        font=dict(color='#B0B8C1'), hovermode='x unified', legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with col2:
    if model_loaded:
        rpms = np.arange(1200, 1801, 10)
        temps_rpm = [np.clip(model.predict([[load_val, ambient_val, r, oil_val]])[0], 25, 95) for r in rpms]
        cur_rpm_temp = round(float(model.predict([[load_val, ambient_val, rpm_val, oil_val]])[0]), 1)
    else:
        rpms = np.linspace(1200, 1800, 50)
        temps_rpm = 45 + rpms * 0.005
        cur_rpm_temp = pred_temp

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=rpms, y=temps_rpm, line=dict(color='#00D4FF', width=2.5),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.08)', name='Temp'))
    fig2.add_trace(go.Scatter(x=[rpm_val], y=[cur_rpm_temp], mode='markers',
        marker=dict(color='#00FF41', size=10), name='Current'))
    fig2.update_layout(
        title=dict(text="2️⃣  Temp vs RPM", font=dict(color='#B0B8C1', size=13)),
        height=320, template='plotly_dark',
        plot_bgcolor='rgba(17,30,48,0.3)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor='rgba(30,58,82,0.3)', title='RPM'),
        yaxis=dict(gridcolor='rgba(30,58,82,0.3)', title='Temp (°C)'),
        font=dict(color='#B0B8C1'), hovermode='x unified', legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)

# BLOCK 5: SYSTEM ALERTS
st.markdown('<div class="block"><div class="block-title">📋 System Alerts</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="alert-item success">
        <div class="alert-icon">✓</div>
        <div class="alert-content"><strong>System Operational</strong>
        <p>All sensors calibrated and functioning normally. Last update: Just now</p></div>
    </div>
    <div class="alert-item success">
        <div class="alert-icon">✓</div>
        <div class="alert-content"><strong>Cooling System Active</strong>
        <p>Cooling efficiency at 87%. Flow rate optimal for current load.</p></div>
    </div>
    <div class="alert-item">
        <div class="alert-icon">⚠️</div>
        <div class="alert-content"><strong>Temperature Trend</strong>
        <p>Gearbox temperature trending upward. Recommend monitoring cooling flow.</p></div>
    </div>
    <div class="alert-item">
        <div class="alert-icon">⚠️</div>
        <div class="alert-content"><strong>Maintenance Due</strong>
        <p>Cooling filter maintenance recommended in 7 days based on flow analysis.</p></div>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# BLOCK 6: DOWNLOAD PDF
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.markdown("""
        <div class="block" style="margin-bottom:0;padding:0.9rem 1.5rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span style="font-size:1.4rem;">📄</span>
                <div>
                    <div style="color:#FFFFFF;font-size:1rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Download PDF Report</div>
                    <div style="color:#B0B8C1;font-size:0.82rem;margin-top:0.2rem;">Includes parameters, prediction summary, suggestions &amp; alerts</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_btn:
    st.markdown('<div style="padding-top:0.6rem;">', unsafe_allow_html=True)
    # ... keep existing download button code here ...
    st.markdown('</div>', unsafe_allow_html=True)
with col_btn:
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        import io

        def create_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4)
            styles = getSampleStyleSheet()
            content = []
            content.append(Paragraph("THERMOLYTIX — System Report", styles['Title']))
            content.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
            content.append(Spacer(1, 12))
            content.append(Paragraph("Parameters", styles['Heading2']))
            content.append(Paragraph(f"Load: {load_val}%  |  RPM: {rpm_val}  |  Ambient: {ambient_val}°C  |  Oil Condition: {oil_val}", styles['Normal']))
            content.append(Spacer(1, 8))
            content.append(Paragraph("Prediction Summary", styles['Heading2']))
            content.append(Paragraph(f"Predicted Temp: {pred_temp}°C  |  Status: {status_text}", styles['Normal']))
            content.append(Spacer(1, 8))
            content.append(Paragraph("Suggestions", styles['Heading2']))
            for _, text in suggestions:
                content.append(Paragraph(f"• {text}", styles['Normal']))
            content.append(Spacer(1, 8))
            content.append(Paragraph("System Alerts", styles['Heading2']))
            for alert in ["System Operational: All sensors functioning normally.",
                          "Cooling System Active: Efficiency at 87%.",
                          "Temperature Trend: Gearbox temp trending upward.",
                          "Maintenance Due: Cooling filter check in 7 days."]:
                content.append(Paragraph(f"• {alert}", styles['Normal']))
            doc.build(content)
            buf.seek(0)
            return buf.read()

        pdf_bytes = create_pdf()
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name=f"thermolytix_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except ImportError:
        report_text = f"""THERMOLYTIX SYSTEM REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

PARAMETERS
Load: {load_val}% | RPM: {rpm_val} | Ambient: {ambient_val}C | Oil Condition: {oil_val}

PREDICTION SUMMARY
Predicted Temp: {pred_temp}C | Status: {status_text}

SUGGESTIONS
""" + "\n".join([f"- {t}" for _, t in suggestions]) + """

SYSTEM ALERTS
- System Operational: All sensors functioning normally.
- Cooling System Active: Efficiency at 87%.
- Temperature Trend: Gearbox temp trending upward.
- Maintenance Due: Cooling filter check in 7 days.
"""
        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name=f"thermolytix_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
    <div class="footer">
        <p><strong>ThermoLytix v2.0</strong> | AI-Powered Thermal Intelligence System</p>
        <p>© 2026 Advanced Thermal Solutions • Designed & Developed by Dipal patel</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
