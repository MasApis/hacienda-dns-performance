
#!/usr/bin/env python3
"""Pengumpul data DNS - Hacienda Del Part."""

import argparse
import csv
import random
import re
import string
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path

import dns.exception
import dns.resolver

DOMAINS = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "wikipedia.org",
    "tokopedia.com",
    "shopee.co.id",
    "detik.com",
    "kompas.com",
    "github.com",
]

TIMEOUT = 3.0
JEDA = 0.3

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data" / "raw" / "dns_data.csv"
)

KOLOM = [
    "run_id",
    "timestamp",
    "sesi",
    "putaran",
    "resolver",
    "ip_resolver",
    "domain",
    "jenis_cache",
    "query_name",
    "waktu_ms",
    "status",
    "rtt_ms",
]


def tentukan_sesi(jam):
    if 5 <= jam <= 10:
        return "pagi"
    if 11 <= jam <= 17:
        return "siang"
    return "malam"


def nama_acak(domain):
    karakter = string.ascii_lowercase + string.digits
    acak = "".join(
        random.choices(karakter, k=16)
    )
    return f"{acak}.{domain}"


def ukur_rtt(ip):
    try:
        hasil = subprocess.run(
            ["ping", "-n", "-c", "3", "-W", "2", ip],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

        pola = re.search(
            r"=\s*[\d.]+/([\d.]+)/",
            hasil.stdout,
        )

        if pola:
            return round(float(pola.group(1)), 3)

    except (OSError, subprocess.TimeoutExpired):
        pass

    return None


def buat_resolver(ip):
    resolver = dns.resolver.Resolver(
        configure=False
    )
    resolver.nameservers = [ip]
    resolver.timeout = TIMEOUT
    resolver.lifetime = TIMEOUT
    return resolver


def query(resolver, nama):
    mulai = time.perf_counter()

    try:
        resolver.resolve(
            nama,
            "A",
            raise_on_no_answer=True,
            search=False,
        )
        status = "ok"

    except dns.resolver.NXDOMAIN:
        status = "nxdomain"

    except dns.resolver.NoAnswer:
        status = "noanswer"

    except dns.exception.Timeout:
        status = "timeout"

    except dns.resolver.NoNameservers:
        status = "no_nameservers"

    except Exception as error:
        status = "error_" + type(error).__name__

    waktu_ms = (
        time.perf_counter() - mulai
    ) * 1000

    return round(waktu_ms, 3), status


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--isp",
        required=True,
        help="IP resolver DNS bawaan jaringan",
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--sesi",
        choices=["pagi", "siang", "malam"],
    )

    args = parser.parse_args()

    if args.rounds < 1:
        parser.error("--rounds harus minimal 1")

    sekarang = datetime.now()
    sesi = args.sesi or tentukan_sesi(
        sekarang.hour
    )

    run_id = uuid.uuid4().hex[:12]

    resolvers = {
        "google": "8.8.8.8",
        "cloudflare": "1.1.1.1",
        "isp": args.isp,
    }

    objek = {
        nama: buat_resolver(ip)
        for nama, ip in resolvers.items()
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_baru = (
        not OUTPUT.exists()
        or OUTPUT.stat().st_size == 0
    )

    total = 0

    with OUTPUT.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=KOLOM,
        )

        if file_baru:
            writer.writeheader()

        for putaran in range(
            1, args.rounds + 1
        ):
            rtt = {
                nama: ukur_rtt(ip)
                for nama, ip in resolvers.items()
            }

            domains = DOMAINS.copy()
            random.shuffle(domains)

            for domain in domains:
                urutan = list(resolvers)
                random.shuffle(urutan)

                for nama in urutan:
                    resolver = objek[nama]
                    ip = resolvers[nama]

                    # Kondisi 1:
                    # Query subdomain acak
                    qname = nama_acak(domain)

                    ms, status = query(
                        resolver, qname
                    )

                    writer.writerow({
                        "run_id": run_id,
                        "timestamp": datetime.now().isoformat(
                            timespec="seconds"
                        ),
                        "sesi": sesi,
                        "putaran": putaran,
                        "resolver": nama,
                        "ip_resolver": ip,
                        "domain": domain,
                        "jenis_cache": "acak",
                        "query_name": qname,
                        "waktu_ms": ms,
                        "status": status,
                        "rtt_ms": rtt[nama],
                    })

                    total += 1
                    time.sleep(JEDA)

                    # Kondisi 2:
                    # Pemanasan lalu query ulang
                    query(resolver, domain)
                    time.sleep(JEDA)

                    ms, status = query(
                        resolver, domain
                    )

                    writer.writerow({
                        "run_id": run_id,
                        "timestamp": datetime.now().isoformat(
                            timespec="seconds"
                        ),
                        "sesi": sesi,
                        "putaran": putaran,
                        "resolver": nama,
                        "ip_resolver": ip,
                        "domain": domain,
                        "jenis_cache": "ulang",
                        "query_name": domain,
                        "waktu_ms": ms,
                        "status": status,
                        "rtt_ms": rtt[nama],
                    })

                    total += 1
                    time.sleep(JEDA)

            file.flush()

            print(
                f"Putaran {putaran}/"
                f"{args.rounds} selesai. "
                f"Total: {total} baris"
            )

    print("\nPengukuran selesai.")
    print(f"Run ID: {run_id}")
    print(f"Sesi: {sesi}")
    print(f"Total observasi: {total}")
    print(f"Dataset: {OUTPUT}")


if __name__ == "__main__":
    main()

