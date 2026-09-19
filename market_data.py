"""Official Korean market-index snapshot from the public data portal."""
from __future__ import annotations

import os
from datetime import date, timedelta
from urllib.parse import unquote

import requests
import streamlit as st


URL = "https://apis.data.go.kr/1160100/service/GetMarketIndexInfoService/getStockMarketIndex"


def _number(value):
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _items(payload):
    response = payload.get("response", {})
    header = response.get("header", {})
    if str(header.get("resultCode")) not in ("00", "0"):
        raise RuntimeError(header.get("resultMsg") or "시장지수 API 오류")
    item = ((response.get("body") or {}).get("items") or {}).get("item", [])
    if isinstance(item, dict):
        return [item]
    return item or []


@st.cache_data(ttl=900, show_spinner=False)
def load_market_indices():
    """Return KOSPI/KOSDAQ snapshots; failures are data, not page-breaking errors."""
    key = unquote(os.getenv("DATA_GO_KR_SERVICE_KEY", "").strip())
    if not key:
        return {"rows": [], "error": "공공데이터포털 서비스키가 필요합니다."}

    try:
        for days in range(10):
            target = (date.today() - timedelta(days=days)).strftime("%Y%m%d")
            response = requests.get(
                URL,
                params={
                    "serviceKey": key,
                    "resultType": "json",
                    "numOfRows": 100,
                    "pageNo": 1,
                    "basDt": target,
                },
                timeout=(8, 20),
            )
            response.raise_for_status()
            rows = _items(response.json())
            selected = []
            for wanted, aliases in {
                "KOSPI": ("코스피", "KOSPI"),
                "KOSDAQ": ("코스닥", "KOSDAQ"),
            }.items():
                match = next(
                    (row for row in rows if str(row.get("idxNm", "")).strip().upper() in {x.upper() for x in aliases}),
                    None,
                )
                if match:
                    selected.append(
                        {
                            "name": wanted,
                            "date": str(match.get("basDt") or target),
                            "close": _number(match.get("clpr")),
                            "change": _number(match.get("vs")),
                            "rate": _number(match.get("fltRt")),
                            "open": _number(match.get("mkp")),
                            "high": _number(match.get("hipr")),
                            "low": _number(match.get("lopr")),
                        }
                    )
            if selected:
                return {"rows": selected, "error": None}
        return {"rows": [], "error": "최근 10일 내 시장지수 자료가 없습니다."}
    except (requests.RequestException, ValueError, KeyError, RuntimeError) as error:
        return {"rows": [], "error": f"시장지수 연결 확인 필요 · {error}"}

