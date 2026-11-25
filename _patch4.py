"""Patch sekali-jalan: pasang gerbang kepemilikan di _check.py.

Sebelumnya syarat "nomor harus milik sendiri" hanya dijaga lewat percakapan.
Sekarang dijaga oleh kode: tanpa flag --milik-saya, mode live menolak jalan
dan tidak mengirim satu request pun.
"""

from pathlib import Path

p = Path(__file__).resolve().parent / "_check.py"
lines = p.read_text(encoding="utf-8").splitlines()

NEW_MAIN = [
    "def main() -> int:",
    "    argv = [a.strip() for a in sys.argv[1:]]",
    "    if not argv:",
    '        print("pakai: python _check.py --dry-run")',
    '        print("       python _check.py --milik-saya 08xxxxxxxxxx")',
    "        return 2",
    '    if any(a in ("--dry-run", "-n", "dry") for a in argv):',
    "        return dry_run()",
    '    owner_ok = "--milik-saya" in argv',
    '    nums = [a for a in argv if not a.startswith("-")]',
    "    if not nums:",
    '        print("pakai: python _check.py --milik-saya 08xxxxxxxxxx")',
    "        return 2",
    "    if not owner_ok:",
    '        print("DITOLAK: mode live hanya untuk nomor milik sendiri.")',
    '        print("Tambahkan flag --milik-saya bila nomor itu benar milik kamu,")',
    '        print("atau bila kamu punya izin tertulis dari pemiliknya.")',
    '        print("Tidak ada request yang dikirim.")',
    "        return 3",
    "    return live(nums[0])",
]

start = None
end = None
for i, line in enumerate(lines):
    if line.startswith("def main() -> int:"):
        start = i
    if start is not None and line.startswith("if __name__"):
        end = i
        break

if start is None or end is None:
    print("FAIL: blok main() tidak ditemukan")
else:
    already = any('"--milik-saya" in argv' in line for line in lines)
    if already:
        print("SKIP: gerbang kepemilikan sudah ada")
    else:
        lines[start:end] = NEW_MAIN + ["", ""]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"OK gerbang kepemilikan dipasang di baris {start + 1}")
        print(f"OK jumlah baris sekarang: {len(lines)}")
