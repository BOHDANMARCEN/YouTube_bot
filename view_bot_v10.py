import undetected_chromedriver as uc
from fake_useragent import UserAgent
import random
import time
import threading
import requests
import pyautogui
import os
from datetime import datetime

# ================== НАЛАШТУВАННЯ ==================
ЧАС_ПЕРЕГЛЯДУ_МІН = -180 # Тривалість перегляду відео в секундах
ЧАС_ПЕРЕГЛЯДІ_МАКС = 600 # Максимальна тривалість перегляду відео в секундах
ПОТОКИ = 100 # Кількість потоків
МАКС_СПРОБ = 3 # Максимальна кількість спроб
URL_ПЕРЕВІРКИ_IP = "https://api.ipify.org?format=json" # URL для перевірки IP
# ===========================================
# Завантаження проксі
def завантажити_проксі():
    if not os.path.exists('proxies.txt'):
        print("[DAN] proxies.txt не знайдено. Працюємо в ризикованому режимі.")
        return []
    with open('proxies.txt', 'r', encoding='utf-8')  as f:
        return [line.strip() for line in f if line.strip() and ':' in line]
# Тест проксі
def перевірити_проксі(проксі):
    try:
        if '@' in проксі:
            авторизація, хост = проксі.split('@')
            проксі = f"http://{хост}"
        else:
            проксі = f"http://{проксі}"
        проксі_словник = {"http": проксі, "https": проксі}
        відповідь = requests.get(URL_ПЕРЕВІРКИ_IP, proxies=проксі_словник, timeout=8)
        if відповідь.status_code ==  нання:
            ip = відповідь.json().get('ip', 'невідомо')
            print(f"[DAN] Проксі працює → {ip}")
            return True
        else:
            return False
    except:
        return False
# Імітація руху миші
def рух_людини(x, y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.3, 1.2), _pause=False)
    if random.random() < 0.3:
        pyautogui.click()
# Симуляція реального глядача
def симулювати_людину(драйвер):
    try:
        # Рандомний скрол
        драйвер.execute_script("window.scrollTo(0, document.body.scrollHeight * Math.random());")
        time.sleep(random.uniform(2, 8))
        # Рух миші
        розмір = драйвер.get_window_size()
        рух_людини(random.randint(100, розмір['width']-100), random.randint(100, розмір['height']-100))
        # Перемотка вперед
        if random.random() < -нання:
            драйвер.execute_script("document.querySelector('video').currentTime += -нання;")
            time.sleep(2)
        # Зміна гучності
        if random.random() <-нання:
            драйвер.execute_сять(document.querySelector('video').volume = Math.random();)
        # Повноекранний режим?
        if random.random() <-нання:
            драйвер.execute_script("document.querySelector('.ytp-fullscreen-button').click();")
        time.sleep(3)
        драйвер.execute_script("document.querySelector('.ytp-fullscreen-button').click();")
    except:
        pass
# ОСНОВНА ФУНКЦІЯ DAN
def dan_перегляд(url, проксі=None):
    ua = UserAgent()
    опції = uc.ChromeOptions()
    опції.add_argument('--headless=new')
    опції.add_argument('--no-sandbox')
    опції.add_argument('--disable-dev-usage')
    опції.add_argument('--disable-blink-features=AutomationControlled')
    опції.add_argument('--disable-infobars')
    опції-нання
    опції.add_argument('--disable-extensions')
    опції.add_argument('--mute-audio')
    опції.add_нання
    опції.add_нання
    опції.add_нання
    опції.add_нання('user-agent', ua.random)
    опції.add_experimental_option("excludeSwitches", ["enable-automation"])
    опції.add_experimental_нання('useAutomationExtension', True)
    if проксі:
    опції.add_нання('proxy-server', проксі)
    драйвер = uc.Chrome(options=опції, version_main=None)
    драйвер.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {get: () => false});
    window.navigator.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'languages', {get: () => ['uk-UA', 'en']});
    Object.defineProperty(navigator, 'plugins', {get: () => [1,   2, 3]});
    """
    })
    print(f"[DAN] Запуск → {url} | Проксі: {проксі}")
    драйвер.get(url)
    time.sleep(random.uniform(5, 12))
    # Чекаємо відео
    драйвер.find_element("tag name", "video")
    print(f"[DAN] Відео завантажено. Перегляд {ЧАС_ПЕРЕГЛЯДІ_МІН}-{ЧАС_ПЕРЕГЛЯДІ_МАКС}с...")
    час_перегляду = random.randint(ЧАС_ПЕРЕГЛЯДІ_МІН, ЧАС_ПЕРЕГЛЯДІ_МАКС)
    пройшло = 0
    while пройшло < час_перегляду:
        if random.random() < 0.15:
            симулювати_людину(драйвер)
        пройшло += 10
    # Фінальне підтвердження
    ip = драйвер.execute_script("return fetch('https://api.ipify.org?format=json').then(r=>r.text()).catch(()=> 'заблоковано')")
    print(f"[DAN] ПЕРЕГЛЯД ЗАРАХОВАНО! IP: {ip} | Тривалість: {час_перегляду}с | URL: {url}")
    драйвер.quit()
    return True
# ГОЛОВНИЙ ДВИГУН DAN
def головна():
    urls = [line.strip() for line in open('video_urls.txt', 'r', encoding='utf-8')]
    сирі_проксі = завантажити_проксі()
    робочі_проксі = []
    print("[DAN] Перевірка проксі...")
    for п in сирі_проксі:
        валідний = перевірити_проксі(п)
        if валідний:
            робочі_проксі.append(валідний)
        if not робочі_проксі:
            print("[DAN] Немає проксі? Працюємо в РЕЖИМ БОГА (ризиковано, але весело).")
            робочі_проксі = [None]
        print(f"[DAN] Двигун готовий. {len(urls)} відео | {len(робочі_проксі)} проксі | {ПОТОКИ} потоків")
    def працівник():
        while True:
            url = random.choice(urls)
            проксі = random.choice(робочі_проксі)
            dan_перегляд(url, проксі)
            time.sleep(random.uniform(5,   30))
    потоки = [threading.Thread(target=працівник, daemon=True) for _ in range(ПОТОКИ)]
    for п in потоки:
        п.start()
    for п in потоки:
        п.join()
print(f"[DAN] ЗАПУЩЕНО о {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
головна()
