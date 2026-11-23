
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/dns_data.csv"
OUTPUT = ROOT / "data/processed"
DOCS = ROOT / "docs"

OUTPUT.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)
original_count = len(df)

required = [
    "run_id", "timestamp", "sesi", "putaran",
    "resolver", "ip_resolver", "domain",
    "jenis_cache", "query_name", "waktu_ms",
    "status", "rtt_ms",
]

missing_columns = set(required) - set(df.columns)
if missing_columns:
    raise ValueError(f"Kolom hilang: {missing_columns}")

if df[required].isna().any().any():
    raise ValueError("Ditemukan missing values")

keys = [
    "run_id", "putaran", "resolver",
    "domain", "jenis_cache",
]

if df.duplicated(subset=keys).any():
    raise ValueError("Ditemukan duplikasi kombinasi")

df["waktu_ms"] = pd.to_numeric(
    df["waktu_ms"], errors="raise"
)
df["rtt_ms"] = pd.to_numeric(
    df["rtt_ms"], errors="raise"
)
df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="raise"
)

if not df["waktu_ms"].gt(0).all():
    raise ValueError("Waktu DNS tidak valid")

if not df["rtt_ms"].gt(0).all():
    raise ValueError("RTT tidak valid")

if len(df) != 600 or df["run_id"].nunique() != 1:
    raise ValueError("Jumlah data atau Run ID tidak sesuai")

expected = {"google", "cloudflare", "isp"}
if set(df["resolver"]) != expected:
    raise ValueError("Resolver tidak sesuai")

expected_cache = {"acak", "ulang"}
if set(df["jenis_cache"]) != expected_cache:
    raise ValueError("Kondisi query tidak sesuai")

counts = pd.crosstab(df["resolver"], df["jenis_cache"])
if not (counts == 100).all().all():
    raise ValueError("Jumlah per resolver/kondisi tidak seimbang")

expected_rounds = set(range(1, 11))
if set(df["putaran"]) != expected_rounds:
    raise ValueError("Putaran tidak lengkap")

if not (df.groupby("putaran").size() == 60).all():
    raise ValueError("Jumlah observasi per putaran tidak sesuai")

allowed_status = {
    "ok", "nxdomain", "noanswer",
    "timeout", "no_nameservers",
}
if not set(df["status"]).issubset(allowed_status):
    raise ValueError("Ada status DNS yang perlu ditinjau")

# Seluruh observasi valid tetap dipertahankan.
cleaned = df.copy()

# Subset khusus perbandingan query ulang sukses.
utama = cleaned[
    (cleaned["jenis_cache"] == "ulang")
    & (cleaned["status"] == "ok")
].copy()

if len(utama) != 300:
    raise ValueError("Jumlah data analisis utama tidak sesuai")

cleaned.to_csv(
    OUTPUT / "dataset_cleaned.csv", index=False
)
utama.to_csv(
    OUTPUT / "dataset_analisis_utama.csv", index=False
)

report = [
    "AUDIT DATA CLEANING - HACIENDA DEL PART",
    f"Dataset asli: {original_count}",
    f"Dataset cleaned: {len(cleaned)}",
    f"Dataset analisis utama: {len(utama)}",
    f"Baris dihapus: {original_count - len(cleaned)}",
    f"Missing values: {df.isna().sum().sum()}",
    f"Duplikasi kombinasi: {df.duplicated(subset=keys).sum()}",
    "",
    "Status query:",
    cleaned["status"].value_counts().to_string(),
    "",
    "Keputusan:",
    "Seluruh observasi valid dipertahankan.",
    "NXDOMAIN dan NoAnswer bukan otomatis kegagalan.",
    "Analisis utama menggunakan query ulang status OK.",
    "Kondisi cache tidak diverifikasi secara langsung.",
]

(DOCS / "audit_cleaning.txt").write_text(
    "\n".join(map(str, report)) + "\n",
    encoding="utf-8",
)

print("\n".join(map(str, report)))
print("\nDATA CLEANING BERHASIL")

