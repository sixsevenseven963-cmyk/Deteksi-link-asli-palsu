import os
import urllib.parse

OFFICIAL_DOMAINS = {
    "dana": ["dana.id"],
    "gopay": ["gopay.co.id"],
    "ovo": ["ovo.id"],
    "shopee": ["shopee.co.id", "shopee.com"],
}

URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "cutt.ly",
    "is.gd",
    "s.id",
}

SUSPICIOUS_TLDS = {
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
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(r"""
╔══════════════════════════════════════════════════════════════╗
║   ██████╗██╗  ██╗ █████╗  ██████╗ ███████╗                  ║
║  ██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔════╝                  ║
║  ██║     ███████║███████║██║   ██║███████╗                  ║
║  ██║     ██╔══██║██╔══██║██║   ██║╚════██║                  ║
║  ╚██████╗██║  ██║██║  ██║╚██████╔╝███████║                  ║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝                  ║
║                                                            ║
║              LINK SCANNER v3.0                             ║
║          HEURISTIC URL RISK ANALYZER                       ║
╚══════════════════════════════════════════════════════════════╝
""")


def is_official_domain(domain):
    for domains in OFFICIAL_DOMAINS.values():
        for official in domains:
            if domain == official or domain.endswith("." + official):
                return True
    return False


def scan_link(url):
    url = url.strip()

    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urllib.parse.urlparse(url)

        domain = (parsed.hostname or "").lower()
        path = parsed.path.lower()

        if not domain:
            raise ValueError

    except Exception:
        return {
            "status": "ERROR",
            "score": 0,
            "domain": "",
            "url": url,
            "reasons": ["Format URL tidak valid."]
        }

    score = 0
    reasons = []

    # Unicode / Homograph
    if any(ord(ch) > 127 for ch in domain):
        score += 3
        reasons.append(
            "Domain menggunakan karakter non-ASCII (perlu verifikasi tambahan)."
        )

    # URL Shortener
    if domain in URL_SHORTENERS:
        score += 3
        reasons.append(
            "Menggunakan layanan URL shortener."
        )

    # APK Download
    if path.endswith(".apk"):
        score += 5
        reasons.append(
            "Link mengarah langsung ke file APK."
        )

    # Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 2
            reasons.append(
                f"Menggunakan TLD berisiko ({tld})."
            )
            break

    # Long Path
    if len(path) > 50:
        score += 1
        reasons.append(
            "Path URL sangat panjang."
        )

    # Suspicious Characters
    if "@" in url:
        score += 3
        reasons.append(
            "Mengandung karakter '@' pada URL."
        )

    # Brand Impersonation
    for brand, domains in OFFICIAL_DOMAINS.items():

        if brand in domain:

            trusted = False

            for official in domains:
                if (
                    domain == official or
                    domain.endswith("." + official)
                ):
                    trusted = True
                    break

            if not trusted:
                score += 5
                reasons.append(
                    f"Nama brand '{brand}' muncul pada domain tidak resmi."
                )

    official = is_official_domain(domain)

    # Verdict
    if score >= 10:
        status = "CRITICAL"
    elif score >= 6:
        status = "HIGH RISK"
    elif score >= 3:
        status = "SUSPICIOUS"
    elif official:
        status = "OFFICIAL"
    else:
        status = "UNKNOWN"

    return {
        "status": status,
        "score": score,
        "domain": domain,
        "url": url,
        "reasons": reasons
    }


def print_result(result):

    if result["status"] == "ERROR":
        print("\n[ERROR]")
        print(result["reasons"][0])
        return

    print("\n" + "=" * 65)
    print(f"URL      : {result['url']}")
    print(f"DOMAIN   : {result['domain']}")
    print(f"SCORE    : {result['score']}")
    print(f"STATUS   : {result['status']}")
    print("=" * 65)

    if result["status"] == "OFFICIAL":
        print("[+] Domain resmi terdeteksi.")

    elif result["status"] == "UNKNOWN":
        print("[?] Tidak ada indikator kuat.")

    elif result["status"] == "SUSPICIOUS":
        print("[!] URL mencurigakan.")

    elif result["status"] == "HIGH RISK":
        print("[!] Risiko tinggi. Perlu verifikasi tambahan.")

    elif result["status"] == "CRITICAL":
        print("[!] Risiko sangat tinggi.")

    if result["reasons"]:
        print("\nAlasan:")
        for i, reason in enumerate(result["reasons"], 1):
            print(f"{i}. {reason}")

    print("=" * 65)


def main():
    clear()
    banner()

    url = input("\nMasukkan URL yang ingin dianalisis: ").strip()

    if not url:
        print("\n[-] URL tidak boleh kosong.")
        return

    result = scan_link(url)
    print_result(result)


if __name__ == "__main__":
    main()
