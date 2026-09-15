from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

url = "https://fvt.com.tr/fonlar/yatirim-fonlari/TLY"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    print(f"Sayfa yükleniyor: {url}")
    driver.get(url)
    
    # Sayfanın tamamen yüklenmesini bekle
    wait = WebDriverWait(driver, 15)
    
    # Hedef elementi CSS selector ile bul
    try:
        target_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.text-sm.font-semibold.tabular-nums.text-\\[\\#0ecb81\\]")
        ))
        value = target_element.text
        print(f"✓ Element bulundu!")
        print(f"Değer: {value}")
    except Exception as e:
        print(f"CSS selector ile bulunamadı: {e}")
        print("\nAlternatif denemeler...")
        
        # XPath ile dene
        try:
            elements = driver.find_elements(By.XPATH, "//span[contains(text(), '%')]")
            for elem in elements:
                text = elem.text
                if text:
                    print(f"  - {text}")
        except Exception as e2:
            print(f"XPath hatası: {e2}")
    
    driver.quit()
    
except Exception as e:
    print(f"Hata: {e}")
    if 'driver' in locals():
        driver.quit()
