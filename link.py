import os
import urllib.parse

# =========================
# CHAOS LINK SCANNER v2.0
# =========================

OFFICIAL_DOMAINS = {
    "dana": ["dana.id"],
    "gopay": ["gopay.co.id"],
    "ovo": ["ovo.id"],
    "shopee": ["shopee.co.id", "shopee.com"],
}

SCAM_KEYWORDS = [
    "dana",
    "gopay",
    "ovo",
    "shopee",
    "hadiah",
    "klaim",
    "claim",
    "undian",
    "bonus",
    "saldo",
    "kaget",
]

SUSPICIOUS_TLDS = [
    ".top",
    ".xyz",
    ".site",
    ".online",
    ".vip",
    ".club",
    ".buzz",
    ".tk",
    ".ml",
    ".ga",
    ".cf",
    ".gq",
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(r"""
██╗     ██╗███╗   ██╗██╗  ██╗
██║     ██║████╗  ██║██║ ██╔╝
██║     ██║██╔██╗ ██║█████╔╝
██║     ██║██║╚██╗██║██╔═██╗
███████╗██║██║ ╚████║██║  ██╗
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

    CHAOS LINK SCANNER v2.0
    URL Safety Analyzer
""")


def is_official_domain(domain):
    for domains in OFFICIAL_DOMAINS.values():
        for official in domains:
            if domain == official or domain.endswith("." + official):
                return True
    return False


def scan_link(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urllib.parse.urlparse(url)

        domain = parsed.netloc.lower()
        path = parsed.path.lower()

    except Exception:
        return {
            "status": "ERROR",
            "reasons": ["Format URL tidak valid."]
        }

    reasons = []
    score = 0

    # APK Detection
    if path.endswith(".apk"):
        reasons.append("Link langsung mengarah ke file APK.")
        score += 5

    # Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            reasons.append(f"Menggunakan TLD mencurigakan ({tld}).")
            score += 2

    # Brand Impersonation
    for brand, official_domains in OFFICIAL_DOMAINS.items():

        if brand in domain:

            trusted = False

            for official in official_domains:
                if domain == official or domain.endswith("." + official):
                    trusted = True
                    break

            if not trusted:
                reasons.append(
                    f"Nama brand '{brand}' muncul pada domain yang bukan domain resmi."
                )
                score += 4

    # Keyword overload
    keyword_count = sum(
        1 for keyword in SCAM_KEYWORDS
        if keyword in domain
    )

    if keyword_count >= 2:
        reasons.append(
            "Terlalu banyak keyword promosi/brand pada domain."
        )
        score += 2

    # Final verdict
    if score >= 6:
        status = "HIGH RISK"
    elif score >= 3:
        status = "SUSPICIOUS"
    elif is_official_domain(domain):
        status = "OFFICIAL"
    else:
        status = "UNKNOWN"

    return {
        "status": status,
        "domain": domain,
        "url": url,
        "score": score,
        "reasons": reasons
    }


def print_result(result):

    if result["status"] == "ERROR":
        print("\n[ERROR]")
        print(result["reasons"][0])
        return

    print("\n" + "=" * 60)
    print(f"URL    : {result['url']}")
    print(f"DOMAIN : {result['domain']}")
    print(f"SCORE  : {result['score']}")
    print("=" * 60)

    if result["status"] == "OFFICIAL":
        print("[+] Domain resmi terdeteksi.")

    elif result["status"] == "HIGH RISK":
        print("[!] RISIKO TINGGI")
        print("Kemungkinan phishing atau penipuan.")

    elif result["status"] == "SUSPICIOUS":
        print("[!] MENCURIGAKAN")
        print("Perlu verifikasi lebih lanjut.")

    else:
        print("[?] DOMAIN TIDAK DIKENAL")
        print("Belum ditemukan indikator kuat.")

    if result["reasons"]:
        print("\nAlasan:")
        for i, reason in enumerate(result["reasons"], 1):
            print(f"{i}. {reason}")

    print("=" * 60)


def main():
    clear()
    banner()

    url = input("\nMasukkan URL: ").strip()

    if not url:
        print("URL tidak boleh kosong.")
        return

    result = scan_link(url)
    print_result(result)


if __name__ == "__main__":
    main()
