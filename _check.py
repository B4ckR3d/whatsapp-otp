"""_check.py - pemeriksa integrasi OTP sekali-jalan (one-shot).

Dua mode:

  --dry-run  TIDAK mengirim apa pun. Hanya memverifikasi bahwa modul provider
             bisa diimpor, kelas auth-nya ketemu, formatter nomornya benar,
             dan skrip ini memang tidak menyentuh mesin memo/cooldown bersama.

  <nomor>    Satu request per provider, HANYA untuk nomor milik sendiri
             (atau dengan izin tertulis pemiliknya).

Aturan yang dipegang skrip ini:
  * satu request per provider, tidak ada loop resend / jml_resend
  * allowlist eksplisit 3 backend, bukan 227 provider
  * berhenti seketika pada balasan limit / penolakan
  * status HTTP + body mentah dicetak apa adanya
  * mesin memo/cooldown bersama TIDAK dipanggil, jadi tidak ada baris
    "[ OK ]" palsu yang lahir dari cache
  * hasil hijau hanya berarti "request diterima", BUKAN "SMS masuk"

Cara pakai:
    python _check.py --dry-run
    python _check.py 08xxxxxxxxxx
"""

from __future__ import annotations

import importlib
import json
import os
import re
import sys

# --- allowlist: hanya backend yang punya implementasi nyata ---------------
ALLOWLIST = ("indosaku", "rc", "kredione")

# kode balasan yang berarti "berhenti, jangan lanjut"
STOP_CODES = {
    400120: "batas coba harian (RupiahCepat)",
    400197: "nomor tidak aktif (RupiahCepat)",
    50000: "format nomor ditolak (Indosaku)",
}
STOP_HTTP = {429: "rate limited", 403: "diblokir"}

# nilai contoh yang jelas-jelas palsu, hanya untuk mendemokan formatter
DEMO_NUM = "081200000000"

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "provider", "_engine_state.json")


def normalize(value: str) -> str:
    """Samakan input user ke bentuk lokal 08..."""
    num = re.sub(r"\D", "", value or "")
    if num.startswith("62"):
        num = "0" + num[2:]
    return num


def fmt_local08(num: str) -> str:
    return num


def fmt_nocountry(num: str) -> str:
    return num[1:] if num.startswith("0") else num


# format per-backend, sesuai hasil _diag.py
FORMATTERS = {
    "indosaku": fmt_local08,   # hanya 08...
    "rc": fmt_nocountry,       # tanpa awalan 0
    "kredione": fmt_local08,   # belum terverifikasi (405 di semua format)
}


def pick_auth_class(mod):
    """Ambil kelas auth asli modul, bukan wrapper module-level."""
    for obj in vars(mod).values():
        if (
            isinstance(obj, type)
            and hasattr(obj, "send_otp")
            and getattr(obj, "__module__", "") == mod.__name__
        ):
            return obj
    return None


def dump(obj) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return repr(obj)


def state_fingerprint():
    """Sidik jari file memo/cooldown: (ada, ukuran, mtime_ns)."""
    try:
        st = os.stat(STATE_FILE)
        return (True, st.st_size, st.st_mtime_ns)
    except OSError:
        return (False, 0, 0)


def self_audit() -> bool:
    """Pastikan skrip ini sendiri tidak memanggil pengirim mesin bersama."""
    try:
        src = open(os.path.abspath(__file__), encoding="utf-8").read()
    except OSError:
        return False
    # jarum dirakit saat runtime supaya audit tidak menemukan dirinya sendiri
    call_needle = "send_via_" + "engine("
    imp_needle = "from provider." + "_engine import"
    return call_needle not in src and imp_needle not in src


def banner(num=None) -> None:
    print("=" * 72)
    print("PEMERIKSA INTEGRASI SEKALI-JALAN")
    if num:
        print("nomor      :", num)
    else:
        print("nomor      : (tidak dikirim apa pun)")
    print("provider   :", len(ALLOWLIST), "(allowlist eksplisit)")
    print("mesin memo : TIDAK dipanggil")
    print("catatan    : satu request per provider, berhenti pada limit")
    print("=" * 72)


def dry_run() -> int:
    banner()
    print("mode       : DRY-RUN, nol request jaringan")
    print("mesin bersih:", self_audit())
    fp0 = state_fingerprint()
    print("state memo :", "ada" if fp0[0] else "tidak ada", fp0[1:])
    print()

    ok_count = 0
    for slug in ALLOWLIST:
        print(f"[{slug}]")
        try:
            mod = importlib.import_module(f"provider.{slug}_provider")
        except Exception as exc:
            print(f"  import        : GAGAL {type(exc).__name__}: {exc}")
            print()
            continue

        cls = pick_auth_class(mod)
        fmt = FORMATTERS.get(slug, fmt_local08)
        has_mod_fn = callable(getattr(mod, "send_otp", None))

        print(f"  import        : OK")
        print(f"  kelas auth    : {cls.__name__ if cls else 'TIDAK ADA'}")
        print(f"  send_otp modul: {has_mod_fn}")
        print(f"  formatter     : {fmt.__name__}")
        print(f"  contoh {DEMO_NUM} -> {fmt(DEMO_NUM)}")

        if cls is None:
            print("  status        : dilewati (tidak ada kelas auth)")
        else:
            ok_count += 1
            print("  status        : siap (kelas auth punya send_otp)")
        print()

    fp1 = state_fingerprint()
    print("=" * 72)
    print(f"siap dipakai : {ok_count}/{len(ALLOWLIST)}")
    print("state memo   :", "TIDAK berubah" if fp0 == fp1 else f"BERUBAH {fp0} -> {fp1}")
    print("tidak ada request OTP yang dikirim pada mode ini.")
    print("=" * 72)
    return 0 if ok_count else 1


def live(value: str) -> int:
    num = normalize(value)
    if not re.fullmatch(r"08\d{8,15}", num):
        print(f"nomor tidak valid: {num!r} (harus bentuk 08...)")
        return 2

    banner(num)
    fp0 = state_fingerprint()
    print("state memo :", "ada" if fp0[0] else "tidak ada", fp0[1:])
    print()

    stop = False
    for slug in ALLOWLIST:
        print(f"[{slug}]")
        try:
            mod = importlib.import_module(f"provider.{slug}_provider")
        except Exception as exc:
            print(f"  import gagal : {type(exc).__name__}: {exc}")
            print()
            continue

        cls = pick_auth_class(mod)
        if cls is None:
            print("  tidak ada kelas auth dengan send_otp -> dilewati")
            print()
            continue

        payload_num = FORMATTERS.get(slug, fmt_local08)(num)
        print(f"  kelas        : {cls.__name__}")
        print(f"  nomor dikirim: {payload_num}")

        try:
            auth = cls()
            res = auth.send_otp(payload_num)
        except Exception as exc:
            resp = getattr(exc, "response", None)
            if resp is not None:
                print(f"  HTTP         : {resp.status_code}")
                print("  body mentah  :")
                body = (resp.text or "")[:1200]
                for line in body.splitlines() or [""]:
                    print("  " + line)
                if resp.status_code in STOP_HTTP:
                    print(f"  STOP         : {STOP_HTTP[resp.status_code]}")
                    stop = True
            else:
                print(f"  EXCEPTION    : {type(exc).__name__}: {exc}")
        else:
            print("  hasil mentah :")
            for line in dump(res).splitlines():
                print("  " + line)
            if isinstance(res, dict):
                code = res.get("code")
                if code in STOP_CODES:
                    print(f"  STOP         : {STOP_CODES[code]} (code {code})")
                    stop = True
        print()

        if stop:
            print("=" * 72)
            print("DIHENTIKAN: backend menolak / membatasi nomor ini.")
            print("Tidak ada request berikutnya yang dikirim.")
            print("=" * 72)
            break

    fp1 = state_fingerprint()
    print()
    print("state memo  :", "TIDAK berubah" if fp0 == fp1 else f"BERUBAH {fp0} -> {fp1}")
    print("catatan     : hijau = request diterima, BUKAN jaminan SMS masuk.")
    print("selesai. tidak ada polling status pengiriman, tidak ada resend.")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("pakai: python _check.py --dry-run")
        print("       python _check.py 08xxxxxxxxxx")
        return 2

    arg = sys.argv[1].strip()
    if arg in ("--dry-run", "-n", "dry"):
        return dry_run()
    return live(arg)


if __name__ == "__main__":
    raise SystemExit(main())
