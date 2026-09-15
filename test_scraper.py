import requests
from bs4 import BeautifulSoup

url = "https://fvt.com.tr/fonlar/yatirim-fonlari/TLY"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Hedef span elementi bul
    target_span = soup.find('span', class_='text-sm font-semibold tabular-nums text-[#0ecb81]')
    
    if target_span:
        value = target_span.get_text(strip=True)
        print(f"✓ Element bulundu!")
        print(f"Değer: {value}")
    else:
        print("✗ Hedef element bulunamadı.")
        print("\nTüm span elementleri kontrol ediliyor...")
        spans = soup.find_all('span')
        for span in spans[:20]:
            text = span.get_text(strip=True)
            if '%' in text or any(c.isdigit() for c in text):
                print(f"  - {text}")
                
except requests.exceptions.RequestException as e:
    print(f"İstek hatası: {e}")
except Exception as e:
    print(f"Hata: {e}")
