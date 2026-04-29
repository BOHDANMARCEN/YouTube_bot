import undetected_chromedriver as uc
from fake_useragent import UserAgent
import random
import time
import threading
import requests
import pyautogui
import os
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouTubeViewBot:
    """Основний клас бота для переглядів YouTube"""
    
    def __init__(self):
        self.config = self.load_config()
        self.proxies = self.load_proxies()
        self.video_urls = self.load_video_urls()
        self.user_agents = self.load_user_agents()
        
    def load_config(self) -> Dict[str, Any]:
        """Завантаження конфігурації з config.json"""
        default_config = {
            "min_view_time": 180,
            "max_view_time": 600,
            "max_attempts": 3,
            "threads_count": 10,
            "proxy_check_url": "https://api.ipify.org?format=json",
            "use_proxies": True,
            "human_behavior": True,
            "random_delays": True,
            "headless_mode": True,
            "log_level": "INFO"
        }
        
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Оновлюємо дефолтні значення
                default_config.update(config)
                return default_config
        except FileNotFoundError:
            logger.warning("config.json не знайдено, використовуються налаштування за замовчуванням")
            return default_config
    
    def load_proxies(self) -> List[str]:
        """Завантаження списку проксі"""
        if not os.path.exists('proxies.txt'):
            logger.warning("proxies.txt не знайдено")
            return []
        
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and ':' in line]
    
    def load_video_urls(self) -> List[str]:
        """Завантаження списку URL відео"""
        if not os.path.exists('video_urls.txt'):
            logger.error("video_urls.txt не знайдено!")
            return []
        
        with open('video_urls.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and 'youtu' in line]
    
    def load_user_agents(self) -> List[str]:
        """Завантаження User-Agent"""
        try:
            if os.path.exists('user_agents.txt'):
                with open('user_agents.txt', 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip()]
            else:
                # Генерація через fake-useragent
                ua = UserAgent()
                return [ua.random for _ in range(100)]
        except:
            return [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            ]
    
    def check_proxy(self, proxy: str) -> Optional[str]:
        """Перевірка працездатності проксі"""
        try:
            if '@' in proxy:
                auth, host = proxy.split('@')
                proxy_url = f"http://{auth}@{host}"
            else:
                proxy_url = f"http://{proxy}"
            
            proxy_dict = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            response = requests.get(
                self.config['proxy_check_url'],
                proxies=proxy_dict,
                timeout=10
            )
            
            if response.status_code == 200:
                ip = response.json().get('ip', 'unknown')
                logger.info(f"Проксі працює → {ip}")
                return proxy_url
                
        except Exception as e:
            logger.error(f"Помилка перевірки проксі {proxy}: {e}")
        
        return None
    
    def human_mouse_movement(self, x: int, y: int):
        """Імітація людського руху миші"""
        pyautogui.moveTo(x, y, duration=random.uniform(0.3, 1.2))
        if random.random() < 0.3:
            pyautogui.click()
    
    def simulate_human_behavior(self, driver):
        """Симуляція людської поведінки"""
        try:
            # Випадковий скрол
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight * Math.random());"
            )
            time.sleep(random.uniform(2, 8))
            
            # Рух миші
            window_size = driver.get_window_size()
            self.human_mouse_movement(
                random.randint(100, window_size['width'] - 100),
                random.randint(100, window_size['height'] - 100)
            )
            
            # Випадкові дії з відео
            if random.random() < 0.4:
                driver.execute_script(
                    "document.querySelector('video').currentTime += 30;"
                )
                time.sleep(2)
            
            if random.random() < 0.3:
                driver.execute_script(
                    "document.querySelector('video').volume = Math.random();"
                )
            
            if random.random() < 0.2:
                fullscreen_buttons = driver.find_elements(
                    "css selector", 
                    '.ytp-fullscreen-button'
                )
                if fullscreen_buttons:
                    fullscreen_buttons[0].click()
                    time.sleep(3)
                    fullscreen_buttons[0].click()
                    
        except Exception as e:
            logger.error(f"Помилка симуляції поведінки: {e}")
    
    def watch_video(self, url: str, proxy: Optional[str] = None) -> bool:
        """Основна функція перегляду відео"""
        # Налаштування Chrome
        options = uc.ChromeOptions()
        
        if self.config['headless_mode']:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--mute-audio')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1366,768')
        options.add_argument(f'--user-agent={random.choice(self.user_agents)}')
        
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = None
        for attempt in range(self.config['max_attempts']):
            try:
                driver = uc.Chrome(options=options, version_main=114)
                
                # Приховування автоматизації
                driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => false});
                    window.navigator.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'languages', {get: () => ['uk-UA', 'en']});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
                    """
                })
                
                logger.info(f"Запуск перегляду → {url}")
                driver.get(url)
                time.sleep(random.uniform(5, 12))
                
                # Очікування завантаження відео
                video_element = driver.find_element("tag name", "video")
                view_time = random.randint(
                    self.config['min_view_time'],
                    self.config['max_view_time']
                )
                
                logger.info(f"Відео завантажено. Час перегляду: {view_time}с")
                
                elapsed = 0
                while elapsed < view_time:
                    if self.config['human_behavior'] and random.random() < 0.15:
                        self.simulate_human_behavior(driver)
                    time.sleep(10)
                    elapsed += 10
                
                # Фінальна перевірка
                try:
                    ip_info = driver.execute_script("""
                        return fetch('https://api.ipify.org?format=json')
                        .then(r => r.json())
                        .then(data => data.ip)
                        .catch(() => 'blocked')
                    """)
                    logger.info(f"Перегляд завершено! IP: {ip_info} | Час: {view_time}с")
                except:
                    logger.info(f"Перегляд завершено! Час: {view_time}с")
                
                driver.quit()
                return True
                
            except Exception as e:
                logger.error(f"Спроба {attempt + 1} невдала: {e}")
                if driver:
                    driver.quit()
                time.sleep(random.uniform(3, 10))
        
        return False
    
    def worker_thread(self):
        """Поток-працівник"""
        working_proxies = []
        
        # Перевірка проксі
        if self.config['use_proxies'] and self.proxies:
            logger.info("Перевірка проксі...")
            for proxy in self.proxies:
                valid_proxy = self.check_proxy(proxy)
                if valid_proxy:
                    working_proxies.append(valid_proxy)
        
        if not working_proxies:
            logger.warning("Немає робочих проксі, працюємо без них")
            working_proxies = [None]
        
        while True:
            try:
                url = random.choice(self.video_urls)
                proxy = random.choice(working_proxies)
                self.watch_video(url, proxy)
                
                if self.config['random_delays']:
                    time.sleep(random.uniform(5, 30))
                    
            except Exception as e:
                logger.error(f"Помилка у потоці: {e}")
                time.sleep(30)
    
    def start(self):
        """Запуск головного двигуна"""
        if not self.video_urls:
            logger.error("Немає URL для перегляду!")
            return
        
        logger.info(f"Запуск двигуна. Відео: {len(self.video_urls)}")
        
        # Створення потоків
        threads = []
        for i in range(self.config['threads_count']):
            thread = threading.Thread(
                target=self.worker_thread,
                daemon=True,
                name=f"Worker-{i}"
            )
            thread.start()
            threads.append(thread)
            time.sleep(1)  # Затримка між запуском
        
        logger.info(f"Запущено {len(threads)} потоків. Ctrl+C для зупинки.")
        
        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            logger.info("Зупинка запитувана користувачем...")

def main():
    """Головна функція"""
    print(f"🚀 УЛЬТРА-НАДІЙНИЙ БОТ ПЕРЕГЛЯДІВ YOUTUBE v10.5")
    print(f"⏰ Запущено о {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    bot = YouTubeViewBot()
    bot.start()

if __name__ == "__main__":
    main()
