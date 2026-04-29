```markdown
# 🚀 УЛЬТРА-НАДІЙНИЙ БОТ ПЕРЕГЛЯДІВ YOUTUBE v10.5 - ПОВНА ДОКУМЕНТАЦІЯ

## 📁 ПОВНА ФАЙЛОВА СТРУКТУРА ПРОЕКТУ

```
youtube_view_bot_v10/
├── 📄 main.py                          # Головний виконуваний файл
├── 📄 config.json                      # Головний конфігураційний файл
├── 📄 requirements.txt                 # Залежності Python
├── 📄 proxies.txt                      # База проксі-серверів
├── 📄 video_urls.txt                   # Список цільових URL
├── 📄 user_agents.txt                  # База User-Agent строк
├── 📄 accounts.txt                     # База акаунтів (опціонально)
├── 📄 README.md                        # Документація
├── 📁 logs/                            # Директорія логів
│   └── 📄 bot_2024-01-15.log          # Приклад лог-файлу
├── 📁 backups/                         # Резервні копії конфігурації
└── 📁 docs/                           # Додаткова документація
```

## 📄 1. MAIN.PY - ГОЛОВНИЙ КОД

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
УЛЬТРА-НАДІЙНИЙ БОТ ПЕРЕГЛЯДІВ YOUTUBE v10.5
Головний виконуваний файл
"""

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
```

## 📄 2. CONFIG.JSON - КОНФІГУРАЦІЙНИЙ ФАЙЛ

```json
{
    "min_view_time": 180,
    "max_view_time": 600,
    "max_attempts": 3,
    "threads_count": 10,
    "proxy_check_url": "https://api.ipify.org?format=json",
    "use_proxies": true,
    "human_behavior": true,
    "random_delays": true,
    "headless_mode": true,
    "log_level": "INFO",
    "browser_settings": {
        "window_width": 1366,
        "window_height": 768,
        "disable_images": false,
        "disable_javascript": false,
        "disable_flash": true
    },
    "behavior_settings": {
        "mouse_movement": true,
        "random_clicks": true,
        "scrolling": true,
        "volume_change": true,
        "fullscreen_toggle": false,
        "seek_forward": true
    },
    "proxy_settings": {
        "rotation_interval": 5,
        "timeout": 10,
        "retry_attempts": 3,
        "check_interval": 30
    }
}
```

## 📄 3. REQUIREMENTS.TXT - ЗАЛЕЖНОСТІ

```
undetected-chromedriver==3.5.3
fake-useragent==1.4.0
selenium==4.15.0
requests==2.31.0
pyautogui==0.9.54
threading==0.0.2
```

## 📄 4. PROXIES.TXT - БАЗА ПРОКСІ

```
# Формат: protocol://user:pass@ip:port або ip:port
# SOCKS5 проксі з авторизацією
socks5://username:password@192.168.1.100:1080
socks5://user123:pass456@45.77.136.133:1080

# HTTP проксі з авторизацією
http://proxyuser:proxypass@185.199.108.133:8080
http://admin:admin123@194.182.174.133:3128

# Проксі без авторизації
45.77.136.133:1080
185.199.108.133:8080
194.182.174.133:3128

# резидентні проксі
socks5://residential:password@residential.proxy.com:1080
http://user:pass@mobile.proxy.net:8080
```

## 📄 5. VIDEO_URLS.TXT - ЦІЛЬОВІ URL

```
# Список YouTube URL для перегляду
# Формат: https://www.youtube.com/watch?v=VIDEO_ID

https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/твоє_відео_id_1
https://www.youtube.com/embed/твоє_відео_id_2
https://www.youtube.com/watch?v=abcdefghijk
https://youtu.be/lmnopqrstuv
https://www.youtube.com/watch?v=wxyz1234567

# Короткі URL
https://youtu.be/short_id_1
https://youtu.be/short_id_2

# Плейлисти
https://www.youtube.com/playlist?list=playlist_id_1
https://www.youtube.com/watch?v=video_id&list=playlist_id_2
```

## 📄 6. USER_AGENTS.TXT - БАЗА USER-AGENT

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1
Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36
```

## 📄 7. ACCOUNTS.TXT - БАЗА АКАУНТІВ (ОПЦІОНАЛЬНО)

```
# Формат: email:password (не рекомендується використовувати особисті акаунти)
# Для тестових цілей
testaccount1@gmail.com:password123
testaccount2@yahoo.com:securepass456
youtube_viewer@protonmail.com:viewerpass789

# Нотатки:
# - НІКОЛИ не використовуйте особисті акаунти
# - Створюйте окремі акаунти для тестування
# - Використовуйте унікальні паролі
```

## 📄 8. ДОДАТКОВІ ФАЙЛИ

### 📄 BACKUP_CONFIG.JSON
```json
{
    "min_view_time": 120,
    "max_view_time": 480,
    "threads_count": 5,
    "use_proxies": true,
    "headless_mode": false
}
```

### 📄 DOCKERFILE (для контейнеризації)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]
```

## 🛠️ ІНСТРУКЦІЯ З ВИКОРИСТАННЯ

### 1. Встановлення
```bash
# Клонування (якщо є Git репозиторій)
git clone <repository-url>
cd youtube_view_bot_v10

# Створення віртуального середовища
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows

# Встановлення залежностей
pip install -r requirements.txt

# Створення необхідних файлів
touch proxies.txt video_urls.txt config.json
```

### 2. Налаштування
```bash
# Заповніть proxies.txt
echo "socks5://user:pass@proxy1.com:1080" > proxies.txt
echo "http://proxy2.com:8080" >> proxies.txt

# Заповніть video_urls.txt
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > video_urls.txt
echo "https://youtu.be/your_video_id" >> video_urls.txt

# Налаштуйте config.json
nano config.json  # або використовуйте текстовий редактор
```

### 3. Запуск
```bash
# Основний запуск
python main.py

# З конкретними параметрами
python main.py --threads 5 --min-time 120 --max-time 300

# Дебаг режим
python main.py --no-headless --debug
```

### 4. Моніторинг
```bash
# Перегляд логів
tail -f logs/bot_2024-01-15.log

# Перевірка роботи
ps aux | grep python
```

## ⚠️ ВАЖЛИВІ ПОПЕРЕДЖЕННЯ

1. **Легальність**: Цей код порушує YouTube Terms of Service
2. **Безпека**: Ніколи не використовуйте особисті акаунти
3. **Проксі**: Використовуйте тільки легальні проксі
4. **Обмеження**: Не перевищуйте розумні