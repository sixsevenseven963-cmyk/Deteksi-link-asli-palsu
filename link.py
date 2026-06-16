import urllib.parse

def scan_link(url):
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
        ".top", ".xyz", ".site", ".online",
        ".vip", ".club", ".buzz",
        ".tk", ".ml", ".ga", ".cf", ".gq"
    }

    url = url.strip()

    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urllib.parse.urlparse(url)

        domain = (parsed.hostname or "").lower()
        path = parsed.path.lower()

        if not domain:
            raise ValueError("Domain kosong")

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

    # ====================
    # Unicode / IDN
    # ====================
    if any(ord(ch) > 127 for ch in domain):
        score += 3
        reasons.append(
            "Domain menggunakan karakter non-ASCII (perlu verifikasi tambahan)."
        )

    # ====================
    # URL Shortener
    # ====================
    if domain in URL_SHORTENERS:
        score += 3
        reasons.append(
            "Menggunakan layanan URL shortener."
        )

    # ====================
    # APK Download
    # ====================
    if path.endswith(".apk"):
        score += 5
        reasons.append(
            "Link mengarah langsung ke file APK."
        )

    # ====================
    # TLD Risk
    # ====================
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 2
            reasons.append(
                f"Menggunakan TLD berisiko ({tld})."
            )
            break

    # ====================
    # Long Path
    # ====================
    if len(path) > 50:
        score += 1
        reasons.append(
            "Path URL sangat panjang."
        )

    # ====================
    # Suspicious Characters
    # ====================
    if "@" in url:
        score += 3
        reasons.append(
            "Mengandung karakter '@' pada URL."
        )

    # ====================
    # Brand Impersonation
    # ====================
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

    # ====================
    # Official Domain Check
    # ====================
    official = False

    for domains in OFFICIAL_DOMAINS.values():
        for off in domains:
            if (
                domain == off or
                domain.endswith("." + off)
            ):
                official = True
                break

    # ====================
    # Verdict
    # ====================
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
