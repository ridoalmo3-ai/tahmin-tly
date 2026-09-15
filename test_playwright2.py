from playwright.sync_api import sync_playwright
import time

url = "https://fvt.com.tr/fonlar/yatirim-fonlari/TLY"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    print(f"Sayfa yükleniyor: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    
    # Sayfanın tamamen yüklenmesi için biraz bekle
    time.sleep(5)
    
    # Sayfa içeriğini al
    html_content = page.content()
    
    # % işareti içeren tüm metinleri bul
    all_text = page.evaluate("() => document.body.innerText")
    
    print("\n=== Sayfadaki % içeren değerler ===")
    for line in all_text.split('\n'):
        if '%' in line and any(c.isdigit() for c in line):
            print(f"  - {line.strip()}")
    
    # Tüm span elementlerini kontrol et
    spans = page.query_selector_all('span')
    print(f"\nToplam span elementi: {len(spans)}")
    
    for i, span in enumerate(spans[:50]):
        text = span.inner_text()
        if text and ('%' in text or '0.' in text):
            class_name = span.get_attribute('class') or ''
            print(f"  [{i}] {text} | class: {class_name[:80]}")
    
    # Sayfanın HTML'ini kaydet
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("\n✓ Sayfa kaynağı 'page_source.html' olarak kaydedildi.")
    
    browser.close()
