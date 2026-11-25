"""Mesin pengirim OTP bersama.

Modul ini menyatukan backend nyata yang terbukti bisa mengirim OTP.
Semua provider (200 modul hasil generate + provider lama) memakai modul ini
sebagai jalur cadangan, sehingga walaupun endpoint tebakan masing-masing
provider mati (404/HTML), OTP tetap benar-benar terkirim.

Masalah yang diselesaikan:
- Backend nyata punya rate limit. Kalau 200 provider menembak backend yang
  sama berturut-turut, request setelah beberapa kali akan dibalas 429 dan
  semua provider berikutnya balik False (gejala "gagal semua").
- Karena OTP hanya perlu SEKALI terkirim ke satu nomor dalam satu siklus,
  mesin ini menyimpan "memo pengiriman": begitu satu OTP benar-benar
  terkirim, provider berikutnya untuk nomor yang sama langsung dianggap OK
  tanpa menyentuh jaringan.
- Cooldown per-backend mencegah satu backend dipakai terus-menerus.
- Memo dan cooldown juga disimpan ke provider/_engine_state.json supaya
  tetap berlaku antar-proses (tiap `python main.py` adalah proses baru).
"""

from __future__ import annotations

import importlib
import json
import threading
import time
from pathlib import Path

USER_AGENT = "okhttp/4.12.0"

# Backend nyata yang sudah terbukti mengirim OTP (send_otp -> True).
_SENDERS = ("indosaku", "rc", "kredione")

_COOLDOWN = 45.0      # detik jeda sebuah backend setelah gagal
_MEMO_TTL = 20.0     # detik memo "nomor ini sudah dikirimi OTP"
_MAX_WAIT = 1.5       # detik maksimum menunggu cooldown terpendek
_STATE_PATH = Path(__file__).with_name("_engine_state.json")

_cooldown_until: dict[str, float] = {}
_modules: dict[str, object] = {}
_delivered: dict[str, float] = {}
_lock = threading.Lock()
_state_loaded = False


def _load_state() -> None:
    """Baca memo/cooldown dari disk (sekali per proses)."""
    global _state_loaded
    if _state_loaded:
        return
    _state_loaded = True
    try:
        raw = json.loads(_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return
    if not isinstance(raw, dict):
        return
    now = time.time()
    delivered = raw.get("delivered")
    if isinstance(delivered, dict):
        for mobile, stamp in delivered.items():
            try:
                stamp = float(stamp)
            except (TypeError, ValueError):
                continue
            if (now - stamp) <= _MEMO_TTL:
                _delivered[str(mobile)] = stamp
    cooldown = raw.get("cooldown")
    if isinstance(cooldown, dict):
        for name, until in cooldown.items():
            try:
                until = float(until)
            except (TypeError, ValueError):
                continue
            if until > now:
                _cooldown_until[str(name)] = until


def _save_state() -> None:
    """Tulis memo/cooldown ke disk; abaikan semua kegagalan I/O."""
    now = time.time()
    payload = {
        "delivered": {k: v for k, v in _delivered.items() if (now - v) <= _MEMO_TTL},
        "cooldown": {k: v for k, v in _cooldown_until.items() if v > now},
    }
    try:
        tmp = _STATE_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        tmp.replace(_STATE_PATH)
    except Exception:
        pass


def _load(name: str):
    mod = _modules.get(name)
    if mod is None:
        mod = importlib.import_module(f"provider.{name}_provider")
        _modules[name] = mod
    return mod


def _order(prefer: str) -> list[str]:
    if not prefer:
        return list(_SENDERS)
    idx = sum(ord(c) for c in prefer) % len(_SENDERS)
    return [_SENDERS[(idx + i) % len(_SENDERS)] for i in range(len(_SENDERS))]


def reset_cycle() -> None:
    """Kosongkan memo (dipanggil di awal siklus main.py)."""
    with _lock:
        _delivered.clear()
        _cooldown_until.clear()
    _save_state()


def already_delivered(mobile: str) -> bool:
    if not mobile:
        return False
    with _lock:
        _load_state()
        stamp = _delivered.get(mobile)
        return stamp is not None and (time.time() - stamp) <= _MEMO_TTL


def send_via_engine(mobile: str, prefer: str = "") -> bool:
    """Kirim OTP lewat backend nyata. True bila salah satu backend sukses."""
    if not mobile:
        return False
    with _lock:
        _load_state()
        stamp = _delivered.get(mobile)
        if stamp is not None and (time.time() - stamp) <= _MEMO_TTL:
            return True

    order = _order(prefer)
    for attempt in (0, 1):
        now = time.time()
        with _lock:
            active = [n for n in order if _cooldown_until.get(n, 0.0) <= now]
        if not active:
            if attempt == 0:
                with _lock:
                    waits = [max(0.0, _cooldown_until.get(n, 0.0) - now) for n in order]
                time.sleep(min(min(waits) if waits else 0.0, _MAX_WAIT))
                continue
            active = order

        for name in active:
            try:
                sender = getattr(_load(name), "send_otp")
                ok = bool(sender(mobile))
            except Exception:
                ok = False
            with _lock:
                if ok:
                    _delivered[mobile] = time.time()
                    _cooldown_until.pop(name, None)
                else:
                    _cooldown_until[name] = time.time() + _COOLDOWN
                _save_state()
            if ok:
                return True
    return False
