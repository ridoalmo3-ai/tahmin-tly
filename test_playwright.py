from playwright.sync_api import sync_playwright

url = "https://fvt.com.tr/fonlar/yatirim-fonlari/TLY"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    print(f"Sayfa yükleniyor: {url}")
    page.goto(url, wait_until="networkidle", timeout=30000)
    
    # Hedef elementi bul
    try:
        element = page.locator("span.text-sm.font-semibold.tabular-nums").first
        value = element.inner_text()
        print(f"✓ Element bulundu!")
        print(f"Değer: {value}")
    except Exception as e:
        print(f"Element bulunamadı: {e}")
        
        # Tüm % içeren elementleri dene
        elements = page.locator("//span[contains(text(), '%')]")
        count = elements.count()
        print(f"\n% içeren span elementleri ({count} adet):")
        for i in range(min(count, 10)):
            text = elements.nth(i).inner_text()
            if text:
                print(f"  - {text}")
    
    browser.close()
