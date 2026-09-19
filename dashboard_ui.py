"""Dense, decision-first dashboard composed only from collected user data."""
from __future__ import annotations

from datetime import date
import html

import altair as alt
import pandas as pd
import streamlit as st


BLUE = "#2563EB"
NAVY = "#163B68"
TEAL = "#0EA5A4"
GREEN = "#059669"
RED = "#EF4444"
MUTED = "#64748B"


def _money(value):
    return f"{float(value):,.0f}원" if value is not None else "자료 없음"


def _panel_title(icon, title, aside=""):
    right = f'<span>{html.escape(aside)}</span>' if aside else ""
    st.markdown(
        f'<div class="decision-title"><b>{icon} {html.escape(title)}</b>{right}</div>',
        unsafe_allow_html=True,
    )


def _position_frame(snapshot):
    rows = []
    for p in (snapshot or {}).get("positions", []):
        cost = float(p.get("average_cost") or 0)
        qty = float(p.get("quantity") or 0)
        value = float(p.get("value") or 0)
        pnl = float(p.get("pnl") or 0)
        invested = value - pnl
        rows.append(
            {
                "종목": p.get("name", p.get("code", "종목")),
                "보유수량": qty,
                "평균매입가": cost,
                "평가액": value,
                "평가손익": pnl,
                "수익률": pnl / invested * 100 if invested > 0 else None,
                "비중": float(p.get("weight") or 0),
            }
        )
    return pd.DataFrame(rows)


def _reports(details):
    return [(stock, report) for stock, report, _, _ in details.values() if report]


def dashboard_overview(details, snapshot):
    """Render a compact portfolio-and-research overview before deep-dive controls."""
    positions = _position_frame(snapshot)
    reports = _reports(details)
    value = float(positions["평가액"].sum()) if not positions.empty else None
    pnl = float(positions["평가손익"].sum()) if not positions.empty else None
    invested = value - pnl if value is not None and pnl is not None else None
    return_pct = pnl / invested * 100 if invested and invested > 0 else None

    st.markdown(
        f"""
<div class="decision-head">
  <div><span class="decision-mark">↗</span><b>오늘의 투자판단</b><small>공시와 재무 데이터를 한 화면에서 확인하세요</small></div>
  <span>{date.today().isoformat()}</span>
</div>
""",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("총 평가자산", _money(value), None if pnl is None else _money(pnl))
    k2.metric("투자원금", _money(invested))
    k3.metric("평가손익", _money(pnl), None if return_pct is None else f"{return_pct:+.2f}%")
    k4.metric("분석된 종목", f"{len(reports)}개", f"관심종목 {len(details)}개")

    main, side = st.columns([2.25, 1], gap="large")
    with main:
        left, right = st.columns([1.18, 1], gap="medium")
        with left, st.container(border=True):
            _panel_title("▦", "보유종목 현황", "계좌 조회 기준")
            if positions.empty:
                st.info("계좌 연결 후 보유수량·평가손익·비중이 여기에 표시됩니다.")
                names = [stock.get("name", "종목") for stock, _ in reports]
                if names:
                    st.caption("현재 분석 종목 · " + " · ".join(names[:8]))
            else:
                shown = positions.copy()
                for col in ["평균매입가", "평가액", "평가손익"]:
                    shown[col] = shown[col].map(lambda x: f"{x:,.0f}")
                shown["수익률"] = shown["수익률"].map(lambda x: "-" if pd.isna(x) else f"{x:+.1f}%")
                shown["비중"] = shown["비중"].map(lambda x: f"{x:.1f}%")
                st.dataframe(shown, hide_index=True, use_container_width=True, height=292)

        with right, st.container(border=True):
            _panel_title("▥", "실적 추이", "DART 확정 결산")
            series = []
            for stock, report in reports:
                for row in report.get("financial", {}).get("years", report.get("years", [])):
                    if row.get("profit") is not None:
                        series.append({"연도": str(row.get("year")), "종목": stock.get("name", "종목"), "영업이익": row["profit"]})
            if series:
                frame = pd.DataFrame(series)
                chart = alt.Chart(frame).mark_line(point=True, strokeWidth=2.4).encode(
                    x=alt.X("연도:O", title=None),
                    y=alt.Y("영업이익:Q", title="영업이익"),
                    color=alt.Color("종목:N", scale=alt.Scale(range=[BLUE, TEAL, "#60A5FA", "#7C3AED"])),
                    tooltip=["종목", "연도", alt.Tooltip("영업이익:Q", format=",")],
                ).properties(height=235)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("종목을 분석하면 연도별 영업이익 추이가 표시됩니다.")

        lower_left, lower_right = st.columns([1, 1], gap="medium")
        with lower_left, st.container(border=True):
            _panel_title("▥", "기업별 성장 비교", "동일 데이터 기준")
            bars = []
            for stock, report in reports:
                years = report.get("years", [])
                if len(years) >= 2 and years[-2].get("revenue") not in (None, 0) and years[-1].get("revenue") is not None:
                    bars.append({"종목": stock.get("name", "종목"), "매출성장률": (years[-1]["revenue"] / years[-2]["revenue"] - 1) * 100})
            if bars:
                frame = pd.DataFrame(bars)
                chart = alt.Chart(frame).mark_bar(cornerRadiusEnd=5, color=TEAL).encode(
                    x=alt.X("매출성장률:Q", title="최근 연간 매출 성장률 (%)"),
                    y=alt.Y("종목:N", sort="-x", title=None),
                    tooltip=["종목", alt.Tooltip("매출성장률:Q", format="+.1f")],
                ).properties(height=180)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("비교 가능한 2개 연도의 재무자료가 필요합니다.")

        with lower_right, st.container(border=True):
            _panel_title("◉", "자산 배분", "평가액 기준")
            if not positions.empty and value and value > 0:
                alloc = positions[["종목", "평가액"]].copy()
                chart = alt.Chart(alloc).mark_arc(innerRadius=58, outerRadius=92).encode(
                    theta=alt.Theta("평가액:Q"),
                    color=alt.Color("종목:N", scale=alt.Scale(range=[BLUE, TEAL, "#F59E0B", "#7C3AED", "#60A5FA"]), legend=alt.Legend(orient="bottom")),
                    tooltip=["종목", alt.Tooltip("평가액:Q", format=",")],
                ).properties(height=205)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("계좌 연결 후 종목별 자산 비중이 표시됩니다.")

    with side:
        with st.container(border=True):
            _panel_title("◎", "오늘의 투자판단", "확정자료 기반")
            if not reports:
                st.info("관심종목을 분석하면 판단 체크포인트가 표시됩니다.")
            else:
                for stock, report in reports[:5]:
                    years = report.get("years", [])
                    recent = years[-1] if years else {}
                    prev = years[-2] if len(years) > 1 else {}
                    if recent.get("profit") is not None and prev.get("profit") not in (None, 0):
                        change = (recent["profit"] / prev["profit"] - 1) * 100
                        signal = "개선" if change > 0 else "둔화"
                        st.markdown(f"**{html.escape(stock.get('name','종목'))}** · 영업이익 {signal} `{change:+.1f}%`")
                    else:
                        st.markdown(f"**{html.escape(stock.get('name','종목'))}** · 실적 비교자료 확인 필요")
                    notices = sorted(report.get("disclosures", []), key=lambda x: x.get("date", ""), reverse=True)
                    if notices:
                        st.caption("최근 공시 · " + notices[0].get("title", "공시 확인"))

        with st.container(border=True):
            _panel_title("▣", "최근 공시", "DART")
            disclosures = []
            for stock, report in reports:
                for notice in report.get("disclosures", []):
                    disclosures.append((notice.get("date", ""), stock.get("name", "종목"), notice))
            for _, name, notice in sorted(disclosures, reverse=True)[:5]:
                label = f"{notice.get('date','')} · {name} · {notice.get('title','공시')}"
                if notice.get("url"):
                    st.link_button(label, notice["url"], use_container_width=True)
                else:
                    st.write(label)
            if not disclosures:
                st.caption("분석된 기업의 최신 공시가 이곳에 표시됩니다.")

        with st.container(border=True):
            _panel_title("✓", "투자 체크포인트")
            checks = [
                "최근 공시의 실적·사업 변화 확인",
                "전년 동기 대비 매출과 영업이익 확인",
                "한 종목 쏠림과 계좌 비중 점검",
                "참고가의 가정과 기준일 확인",
            ]
            for item in checks:
                st.markdown(f'<div class="decision-check">✓ {html.escape(item)}</div>', unsafe_allow_html=True)


def inject_dashboard_css():
    st.markdown(
        """
<style>
.decision-head{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;margin:0 0 12px;background:linear-gradient(105deg,#12375F,#215E97);color:white;border-radius:14px;box-shadow:0 8px 24px rgba(22,59,104,.17)}
.decision-head>div{display:flex;align-items:center;gap:10px}.decision-head b{font-size:22px}.decision-head small{color:#D9EAFE}.decision-head>span{font-size:12px;color:#D9EAFE}.decision-mark{font-size:24px;color:#76D5F3}.decision-title{display:flex;justify-content:space-between;align-items:center;padding-bottom:9px;margin-bottom:8px;border-bottom:1px solid #E5EDF6;color:#17375E}.decision-title b{font-size:16px}.decision-title span{font-size:11px;color:#7B8CA5}.decision-check{padding:7px 0;color:#256B61;font-size:13px;border-bottom:1px dashed #DCE9E5}.decision-check:last-child{border-bottom:0}
@media(max-width:700px){.decision-head small,.decision-head>span{display:none}.decision-head b{font-size:19px}}
</style>
""",
        unsafe_allow_html=True,
    )
