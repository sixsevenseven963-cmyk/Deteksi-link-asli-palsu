import os
import re
import urllib.parse

def print_logo():
    logo = """
\033[91m██╗     ██╗███╗   ██╗██╗  ██╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
██║     ██║████╗  ██║██║  ██║    ██╔════╝██╔════╝██╔══██╗████╗  ██║
██║     ██║██╔██╗ ██║███████║    ███████╗██║     ███████║██╔██╗ ██║
██║     ██║██║╚██╗██║██╔══██║    ╚════██║██║     ██╔══██║██║╚██╗██║
███████╗██║██║ ╚████║██║  ██║    ███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝\033[0m
   \033[92m[+]-- CHAOS LINK SCANNER v1.0 - ANTI-PHISHING TRACER --[+]\033[0m
"""
    print(logo)

def scan_link(url):
    # Bersihkan input url
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.lower()
        path = parsed_url.path.lower()
    except:
        return "\033[91m[-] Format URL tidak valid, Bos!\033[0m"

    print(f"\n\033[94m[*] Menganalisis Target:\033[0m {url}")
    print(f"\033[94m[*] Domain Utama     :\033[0m {domain}")
    print("-" * 60)

    # 1. Daftar Domain Resmi yang Sering Ditiru (White List)
    official_dana = "dana.id"
    
    # Keyword sensitif penipuan
    scam_keywords = ['dana', 'gopay', 'ovo', 'shopee', 'klaim', 'hadiah', 'undian', 'sukses', 'bagisaldo', 'kaget']
    
    # TLD / Ekstensi domain murah yang sering dipakai scammer
    scam_tlds = ['.top', '.xyz', '.site', '.online', '.club', '.vip', '.buzz', '.tk', '.ml', '.ga', '.cf', '.gq', '.apwm']

    is_phishing = False
    alasan = []

    # Cek apakah domain mengandung kata DANA dll tapi BUKAN domain resmi dana.id
    for keyword in scam_keywords:
        if keyword in domain:
            if official_dana not in domain:
                is_phishing = True
                alasan.append(f"Menggunakan nama tiruan '{keyword}' bukan pada situs resminya.")

    # Cek ekstensi domain sampah (.top, .xyz, dll)
    for tld in scam_tlds:
        if domain.endswith(tld) or tld in domain:
            is_phishing = True
            alasan.append(f"Menggunakan ekstensi domain mencurigakan ({tld}) yang biasa dipakai penipuan.")

    # Cek jika link langsung mengarah ke file APK berbahaya
    if path.endswith('.apk'):
        return """\033[41m\033[97m   [ BAHAYA PETAKA: LINK UNDUHAN APK MALWARE ]   \033[0m
\033[91m[!] KESIMPULAN: PALSU & SANGAT BERBAHAYA!\033[0m
\033[93m[Detail]     : Link ini langsung mengunduh file aplikasi (.apk). 
               Besar kemungkinan ini malware peretas SMS/M-Banking (APK Phishing).\033[0m
\033[91m[Tindakan]   : JANGAN DIKLIK, JANGAN DI-INSTALL!\033[0m"""

    # Cetak Hasil Akhir yang Mudah Dipahami
    if is_phishing:
        hasil = f"""\033[41m\033[97m   [ PERINGATAN: LINK PHISHING / PALSU DETECTED ]   \033[0m
\033[91m[!] KESIMPULAN: 100% PALSU / INDIKASI PENIPUAN!\033[0m
\033[93m[Alasan Analisis]:\033[0m"""
        for index, item in enumerate(alasan, 1):
            hasil += f"\n  {index}. {item}"
        hasil += f"\n\n\033[92m[Tips Aman]   : Situs resmi DANA hanya menggunakan domain \033[5m\033[96mdana.id\033[0m\033[92m. Di luar itu FIX MALING DATA.\033[0m"
        return hasil
    else:
        # Peringatan kalau domainnya gak dikenal tapi gak masuk radar blacklist
        if official_dana in domain:
            return """\033[42m\033[97m   [ LINK AMAN / RESMI ]   \033[0m
\033[92m[+] KESIMPULAN: LINK AMAN.\033[0m
\033[92m[Detail]     : Ini adalah domain resmi milik brand terkait.\033[0m"""
        else:
            return """\033[43m\033[30m   [ PERINGATAN: DOMAIN TIDAK DIKENAL ]   \033[0m
\033[93m[!] KESIMPULAN: MENCURIGAKAN (Harus Waspada).\033[0m
\033[93m[Detail]     : Tools tidak menemukan kecocokan domain resmi, namun tidak ada indikasi 
               mendompleng nama DANA. Tetap jangan masukkan data sensitif (No HP/PIN).\033[0m"""

def main():
    os.system('clear')
    print_logo()
    print("=" * 66)
    target_url = input("\033[96m[*] Masukkan URL/Link yang mau di-scan: \033[0m").strip()
    
    if not target_url:
        print("\033[91m[-] Input kosong, Bos!\033[0m")
        return

    hasil_scan = scan_link(target_url)
    print(hasil_scan)
    print("=" * 66)

if __name__ == "__main__":
    main()
