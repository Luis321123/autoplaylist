import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import yt_dlp


def get_video_urls(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True, 
        'force_generic_extractor': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if 'entries' in info:
            return [entry['url'] for entry in info['entries']]
    return []

def open_y2mate_with_urls(urls):
    chrome_options = Options()

    user_data_dir = r"C:\Users\Usuario\AppData\Local\Google\Chrome\User Data"
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("profile-directory=Default")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    service = Service(executable_path=ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )

    driver.get("https://www.y2mate.com")
    print("esperando a que se quite clodflare...")
    input("presiona enter cuando este listo")
    time.sleep(2)

    for url in urls:
        try:
            print(f"Procesando: {url}")
            search_box = driver.find_element(By.ID, "txt-url") 
            search_box.clear()
            search_box.send_keys(url)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5) 
        except Exception as e:
            print(f"Error procesando {url}: {e}")

    driver.quit()

if __name__ == "__main__":
    playlist_url = input("Ingresa la URL de la lista de reproducción de YouTube: ")
    urls = get_video_urls(playlist_url)

    if urls:
        print(f"Se encontraron {len(urls)} videos. Abriendo y2mate.com...")
        open_y2mate_with_urls(urls)
    else:
        print("No se encontraron videos en la lista de reproducción.")
