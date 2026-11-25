"""Provider PUBG Mobile - kirim OTP via endpoint registrasi PUBG Mobile."""
from __future__ import annotations

import requests

from provider._engine import USER_AGENT, send_via_engine

BASE = "https://pubgmobile.com"
LANDING_REFERER = f"{BASE}/register"
API_ENDPOINT = f"{BASE}/api/v1/otp/send"
MSG_TYPE = 1

_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": BASE,
    "Referer": LANDING_REFERER,
    "User-Agent": USER_AGENT,
}


def _payload(mobile: str) -> dict:
    return {
        "mobile": mobile,
        "phone": mobile,
        "msisdn": mobile,
        "msgType": MSG_TYPE,
        "type": "register",
    }


def _is_ok(res: object) -> bool:
    if not isinstance(res, dict):
        return False
    if res.get("result") == 0 or res.get("code") in (0, 200):
        return True
    if res.get("success") is True or str(res.get("rc")) == "00":
        return True
    blob = str(res).lower()
    return any(word in blob for word in ("otp", "success", "berhasil", "terkirim", "sent"))


def _try_local(mobile: str) -> bool:
    session = requests.Session()
    session.headers.update(_HEADERS)
    try:
        session.get(LANDING_REFERER, timeout=6)
    except Exception:
        pass
    try:
        res = session.post(API_ENDPOINT, json=_payload(mobile), timeout=6)
        if res.status_code < 500:
            try:
                if _is_ok(res.json()):
                    return True
            except ValueError:
                pass
    except Exception:
        pass
    return False


def send_otp(mobile: str) -> bool:
    """Kirim OTP ke PUBG Mobile. True bila salah satu jalur berhasil."""
    try:
        if _try_local(mobile):
            return True
    except Exception:
        pass
    return send_via_engine(mobile, prefer="pubgmobile")
