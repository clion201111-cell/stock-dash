from __future__ import annotations

import html

import streamlit as st


NAV_ITEMS = [
    ("홈", "⌂"),
    ("시장 현황", "▥"),
    ("종목 분석", "◫"),
    ("공시 분석", "▤"),
    ("테마 & 섹터", "◇"),
    ("포트폴리오", "▣"),
    ("관심 종목", "☆"),
    ("AI 인사이트", "✦"),
    ("데이터 연결 관리", "⚙"),
]


def apply_theme():
    st.markdown(
        """
<style>
:root {
  --dash-bg:#F3F7FC;
  --dash-surface:#FFFFFF;
  --dash-soft:#F8FBFF;
  --dash-line:#DFE8F3;
  --dash-text:#14233D;
  --dash-muted:#718096;
  --dash-navy:#17375E;
  --dash-blue:#2563EB;
  --dash-teal:#0EA5A4;
  --dash-green:#059669;
  --dash-red:#E5484D;
}
html, body, [class*="css"] {
  font-family:Pretendard,"Noto Sans KR","Apple SD Gothic Neo",sans-serif;
}
.stApp { background:var(--dash-bg)!important; color:var(--dash-text); }
.block-container {
  max-width:1480px!important;
  padding-top:1.25rem!important;
  padding-bottom:3.5rem!important;
}
header[data-testid="stHeader"] {
  background:rgba(243,247,252,.86);
  backdrop-filter:blur(12px);
}
section[data-testid="stSidebar"] {
  background:#FFFFFF!important;
  border-right:1px solid var(--dash-line)!important;
}
section[data-testid="stSidebar"] > div { padding-top:.9rem; }
[data-testid="stSidebar"] .stRadio > label { display:none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap:.25rem; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  margin:1px 0;
  padding:.68rem .72rem;
  border:1px solid transparent!important;
  border-radius:11px;
  transition:background .15s ease,border-color .15s ease;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { background:#F4F7FB; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background:#EFF6FF!important;
  border-color:#BFDBFE!important;
  box-shadow:inset 3px 0 var(--dash-blue)!important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p {
  color:#1D4ED8!important;
  font-weight:750;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p { font-size:14px!important; }
h1,h2,h3,h4 { color:var(--dash-text); letter-spacing:-.035em; }
h1 { font-weight:800; }
h2,h3 { font-weight:760; }
p,li { line-height:1.62; }
[data-testid="stCaptionContainer"] { color:var(--dash-muted); }
[data-testid="stMetric"] {
  background:#FFFFFF!important;
  border:1px solid var(--dash-line)!important;
  border-radius:14px!important;
  padding:16px 18px!important;
  box-shadow:0 6px 20px rgba(20,35,61,.045)!important;
}
[data-testid="stMetricLabel"] { color:var(--dash-muted)!important; }
[data-testid="stMetricValue"] { color:var(--dash-text)!important; font-weight:800!important; }
[data-testid="stVerticalBlockBorderWrapper"] {
  border-color:var(--dash-line)!important;
  border-radius:14px!important;
  background:#FFFFFF!important;
  box-shadow:0 6px 20px rgba(20,35,61,.035)!important;
}
[data-testid="stExpander"] {
  background:#FFFFFF!important;
  border-color:var(--dash-line)!important;
  border-radius:12px!important;
}
.stButton > button,.stFormSubmitButton > button {
  min-height:2.7rem;
  border-radius:10px!important;
  font-weight:700!important;
}
.stButton > button[kind="primary"],.stFormSubmitButton > button[kind="primary"] {
  color:#FFFFFF!important;
  background:var(--dash-blue)!important;
  border-color:var(--dash-blue)!important;
  box-shadow:0 5px 14px rgba(37,99,235,.18);
}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] > div {
  background:#FFFFFF!important;
  border-color:#D6E1EE!important;
  border-radius:11px!important;
}
.stTabs [data-baseweb="tab-list"] { gap:5px; border-bottom:1px solid var(--dash-line); }
.stTabs [data-baseweb="tab"] { padding:9px 13px; border-radius:9px 9px 0 0; font-weight:650; }
.stTabs [aria-selected="true"] { color:var(--dash-blue)!important; border-bottom:2px solid var(--dash-blue)!important; }
.stDataFrame { border:1px solid var(--dash-line)!important; border-radius:12px!important; overflow:hidden; }
.planx-brand { display:flex; align-items:center; gap:10px; margin:4px 0 22px; }
.planx-brand-mark {
  width:38px; height:38px; border-radius:11px;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(135deg,var(--dash-navy),var(--dash-blue));
  color:#FFFFFF; font-size:19px; font-weight:800;
  box-shadow:0 7px 16px rgba(37,99,235,.18);
}
.planx-brand-title { color:var(--dash-text); font-size:19px; line-height:1.15; font-weight:800; letter-spacing:-.03em; }
.planx-brand-sub { margin-top:2px; color:#94A3B8; font-size:10px; letter-spacing:.04em; }
.planx-hero {
  padding:26px 29px;
  margin-bottom:18px;
  overflow:hidden;
  position:relative;
  background:linear-gradient(110deg,#17375E 0%,#1F4F83 58%,#2E74B5 100%);
  border:0;
  border-radius:18px;
  box-shadow:0 13px 30px rgba(23,55,94,.16);
}
.planx-hero:after {
  content:""; position:absolute; width:230px; height:230px; right:-70px; top:-105px;
  border-radius:50%; background:rgba(255,255,255,.07);
}
.planx-eyebrow { margin-bottom:8px; color:#B9D7FF; font-size:11px; font-weight:800; letter-spacing:.11em; text-transform:uppercase; }
.planx-hero h1 { margin:0; color:#FFFFFF!important; font-size:31px; line-height:1.18; }
.planx-hero p { max-width:780px; margin:9px 0 0; color:#DCEBFA; font-size:14px; }
.planx-card {
  min-height:118px;
  padding:17px 18px;
  background:#FFFFFF;
  border:1px solid var(--dash-line);
  border-radius:14px;
  box-shadow:0 6px 20px rgba(20,35,61,.04);
  transition:transform .15s ease,box-shadow .15s ease;
}
.planx-card:hover { transform:translateY(-1px); box-shadow:0 10px 26px rgba(20,35,61,.07); }
.planx-card-title { margin-bottom:8px; color:var(--dash-muted); font-size:12px; font-weight:700; }
.planx-card-value { color:var(--dash-text); font-size:23px; font-weight:800; letter-spacing:-.03em; }
.planx-card-note { margin-top:7px; color:#94A3B8; font-size:11px; }
.planx-empty { padding:22px; color:var(--dash-muted); background:#FFFFFF; border:1px dashed #BFCCE0; border-radius:14px; }
.planx-source { display:inline-flex; align-items:center; gap:5px; padding:4px 8px; color:var(--dash-muted); background:#F8FAFC; border:1px solid #E2E8F0; border-radius:999px; font-size:10px; }
.planx-status-ok { color:#047857; background:#ECFDF5; border-color:#A7F3D0; }
.planx-status-wait { color:#92400E; background:#FFFBEB; border-color:#FDE68A; }
.planx-status-bad { color:#B91C1C; background:#FEF2F2; border-color:#FECACA; }
hr { border-color:var(--dash-line)!important; }
@media (max-width:900px) {
  .block-container { padding-left:1rem!important; padding-right:1rem!important; }
  .planx-hero { padding:22px 20px; }
  .planx-hero h1 { font-size:27px; }
}
@media (max-width:640px) {
  .block-container { padding-top:1rem!important; }
  .planx-card { min-height:100px; padding:14px; }
  .planx-card-value { font-size:21px; }
}
</style>
""",
        unsafe_allow_html=True,
    )


def brand():
    st.markdown(
        """
<div class="planx-brand">
  <div class="planx-brand-mark">↗</div>
  <div>
    <div class="planx-brand-title">StockDash</div>
    <div class="planx-brand-sub">DATA TO INSIGHT</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "PLANX INVESTMENT OS"):
    st.markdown(
        f"""
<div class="planx-hero">
  <div class="planx-eyebrow">{html.escape(eyebrow)}</div>
  <h1>{html.escape(title)}</h1>
  <p>{html.escape(subtitle)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def card(title: str, value: str, note: str = "", status: str = ""):
    status_html = f'<div class="planx-card-note">{html.escape(status)}</div>' if status else ""
    st.markdown(
        f"""
<div class="planx-card">
  <div class="planx-card-title">{html.escape(title)}</div>
  <div class="planx-card-value">{html.escape(value)}</div>
  <div class="planx-card-note">{html.escape(note)}</div>
  {status_html}
</div>
""",
        unsafe_allow_html=True,
    )


def empty_state(title: str, message: str):
    st.markdown(
        f"""
<div class="planx-empty">
  <strong style="color:#334155">{html.escape(title)}</strong><br>
  <span>{html.escape(message)}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def source_badge(label: str, state: str = "wait"):
    cls = {"ok": "planx-status-ok", "bad": "planx-status-bad"}.get(state, "planx-status-wait")
    st.markdown(
        f'<span class="planx-source {cls}">{html.escape(label)}</span>',
        unsafe_allow_html=True,
    )


def apply_final_polish():
    """Backward-compatible no-op for older callers."""
    return None
