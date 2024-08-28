from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging
import random
from fake_useragent import UserAgent
import undetected_chromedriver as uc

VIDEO_URLS = [
    'https://www.youtube.com/yourvid'   # add your Video Link here 
]
WAIT_TIME = random.uniform(5, 15)
COOKIE_ACCEPT_WAIT = 15
AD_SKIP_WAIT = random.uniform(10, 30)

logging.basicConfig(level=logging.INFO)


def scroll_into_view(driver, element):
    """Scrollt ein Element in die Ansicht."""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)


def human_like_delay(min_time=1.0, max_time=3.0):
    """Fügt eine zufällige Verzögerung ein, um menschliche Interaktion zu simulieren."""
    time.sleep(random.uniform(min_time, max_time))


def move_mouse_human_like(driver, element):
    """Simuliert menschenähnliche Mausbewegungen zu einem Element."""
    action = webdriver.ActionChains(driver)
    action.move_to_element(element).perform()

    for _ in range(random.randint(5, 15)):
        x_offset = random.randint(-10, 10)
        y_offset = random.randint(-10, 10)
        action.move_by_offset(x_offset, y_offset).perform()
        human_like_delay(0.05, 0.2)
    
    action.move_to_element(element).click().perform()


def setup_driver():
    """Richtet eine Chrome WebDriver-Instanz mit einer modifizierten User-Agent ein."""
    ua = UserAgent()
    chrome_options = Options()
    chrome_options.add_argument(f"--user-agent={ua.random}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=chrome_options)
    return driver


def handle_cookie_consent(driver):
    """Verarbeitet die Cookie-Zustimmung."""
    try:
        accept_button = WebDriverWait(driver, COOKIE_ACCEPT_WAIT).until(
            EC.visibility_of_element_located((By.XPATH, "//button//span[text()='Alle akzeptieren']"))
        )
        scroll_into_view(driver, accept_button)
        move_mouse_human_like(driver, accept_button)
        logging.info("Cookie-Zustimmung akzeptiert")
    except Exception as e:
        logging.warning(f"Keine Cookie-Zustimmungsdialog gefunden oder Fehler aufgetreten: {e}")


def skip_ads(driver):
    """Überspringt Anzeigen, wenn der Überspringen-Button verfügbar ist."""
    while True:
        try:
            ad_skip_button = WebDriverWait(driver, AD_SKIP_WAIT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button"))
            )
            move_mouse_human_like(driver, ad_skip_button)
            logging.info("Anzeige übersprungen")
            human_like_delay(1, 2)
        except Exception as e:
            logging.info(f"Keine weiteren Anzeigen zum Überspringen oder Fehler aufgetreten: {e}")
            break


def check_for_video_playing(driver):
    """Überprüft, ob das Hauptvideo abgespielt wird."""
    check_ad_playing = driver.execute_script("return document.querySelector('.html5-video-player').classList.contains('ad-showing');")
    return not check_ad_playing


def check_if_video_is_paused(driver):
    """Überprüft, ob das Video momentan pausiert ist."""
    paused = driver.execute_script("return document.querySelector('video').paused;")
    return paused


def play_video(driver, video_url):
    """Spielt das Video von der gegebenen URL ab."""
    driver.get(video_url)
    
    human_like_delay(3, 7)
    handle_cookie_consent(driver)
    
    human_like_delay(2, 5)
    skip_ads(driver)

    while not check_for_video_playing(driver):
        logging.info("Warte auf Start des Hauptvideos...")
        human_like_delay(1, 2)

    if check_if_video_is_paused(driver):
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)
        logging.info("Video war pausiert. Jetzt abspielen.")
    else:
        logging.info("Video läuft bereits.")

    video_duration = driver.execute_script("return document.querySelector('video').duration;")
    logging.info(f"Videodauer: {video_duration} Sekunden")
    
    stop_time = random.uniform(0.7 * video_duration, video_duration)
    logging.info(f"Video wird nach: {stop_time} Sekunden stoppen")

    time.sleep(stop_time)


def random_user_behavior(driver):
    """Simuliert zufälliges Benutzerverhalten."""
    actions = [
        lambda: driver.refresh(),
        lambda: driver.execute_script("window.scrollBy(0, window.innerHeight);"),
        lambda: human_like_delay(10, 20)  
    ]
    random.choice(actions)()


def play_video_loop():
    """Schleife durch die Video-URLs und spielt sie ab."""
    driver = setup_driver()

    try:
        for video_url in VIDEO_URLS:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            play_video(driver, video_url)
            random_user_behavior(driver) 

    except Exception as e:
        logging.error(f"Ein Fehler ist aufgetreten: {e}")

    finally:
        driver.quit()


def main():
    """Hauptfunktion zur Ausführung der Videoschleife."""
    try:
        while True:
            play_video_loop()
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        logging.info("Schleife durch Benutzer unterbrochen. Beende.")


if __name__ == "__main__":
    main()
