import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc

VIDEO_URLS = [
    'https://www.youtube.com/yourvid'  # Füge hier Youtube Video-Link hinzu
]
WAIT_TIME = random.uniform(5, 15)
COOKIE_ACCEPT_WAIT = 15
AD_SKIP_WAIT = random.uniform(10, 30)

logging.basicConfig(level=logging.INFO)


class WebDriverManager:
    """Verwaltet die Einrichtung und das Management des Webdrivers."""

    def __init__(self):
        self.driver = self._setup_driver()

    def _setup_driver(self):
        ua = UserAgent()
        chrome_options = Options()
        chrome_options.add_argument(f"--user-agent={ua.random}")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        return uc.Chrome(options=chrome_options)

    def quit(self):
        self.driver.quit()

    def get_driver(self):
        return self.driver


class VideoPlayer:
    """Verantwortlich für das Abspielen und Verwalten von Videos."""

    def __init__(self, driver):
        self.driver = driver

    def play_video(self, video_url):
        self.driver.get(video_url)
        self._human_like_delay(3, 7)
        self._handle_cookie_consent()
        self._human_like_delay(2, 5)
        self._skip_ads()

        if not self._check_for_video_playing():
            logging.info("Warte auf Start des Hauptvideos...")
            self._human_like_delay(1, 2)

        if self._check_if_video_is_paused():
            self._resume_video()
        else:
            logging.info("Video läuft bereits.")

        self._watch_video()

    def _handle_cookie_consent(self):
        try:
            accept_button = WebDriverWait(self.driver, COOKIE_ACCEPT_WAIT).until(
                EC.visibility_of_element_located((By.XPATH, "//button//span[text()='Alle akzeptieren']"))
            )
            self._scroll_into_view(accept_button)
            self._move_mouse_human_like(accept_button)
            logging.info("Cookie-Zustimmung akzeptiert")
        except Exception as e:
            logging.warning(f"Keine Cookie-Zustimmungsdialog gefunden oder Fehler aufgetreten: {e}")

    def _skip_ads(self):
        while True:
            try:
                ad_skip_button = WebDriverWait(self.driver, AD_SKIP_WAIT).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button"))
                )
                self._move_mouse_human_like(ad_skip_button)
                logging.info("Anzeige übersprungen")
                self._human_like_delay(1, 2)
            except Exception as e:
                logging.info(f"Keine weiteren Anzeigen zum Überspringen oder Fehler aufgetreten: {e}")
                break

    def _check_for_video_playing(self):
        return not self.driver.execute_script(
            "return document.querySelector('.html5-video-player').classList.contains('ad-showing');"
        )

    def _check_if_video_is_paused(self):
        return self.driver.execute_script("return document.querySelector('video').paused;")

    def _resume_video(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)
        logging.info("Video war pausiert. Jetzt abspielen.")

    def _watch_video(self):
        video_duration = self.driver.execute_script("return document.querySelector('video').duration;")
        logging.info(f"Videodauer: {video_duration} Sekunden")

        stop_time = random.uniform(0.7 * video_duration, video_duration)
        logging.info(f"Video wird nach: {stop_time} Sekunden stoppen")
        time.sleep(stop_time)

    def _scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def _move_mouse_human_like(self, element):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(element).perform()

        for _ in range(random.randint(5, 15)):
            x_offset = random.randint(-10, 10)
            y_offset = random.randint(-10, 10)
            action.move_by_offset(x_offset, y_offset).perform()
            self._human_like_delay(0.05, 0.2)

        action.move_to_element(element).click().perform()

    def _human_like_delay(self, min_time=1.0, max_time=3.0):
        time.sleep(random.uniform(min_time, max_time))


class UserBehaviorSimulator:
    """Simuliert zufälliges Benutzerverhalten im Browser."""

    def __init__(self, driver):
        self.driver = driver

    def simulate(self):
        actions = [
            lambda: self.driver.refresh(),
            lambda: self.driver.execute_script("window.scrollBy(0, window.innerHeight);"),
            lambda: self._human_like_delay(10, 20)
        ]
        random.choice(actions)()

    def _human_like_delay(self, min_time=1.0, max_time=3.0):
        time.sleep(random.uniform(min_time, max_time))


class VideoPlaybackLoop:
    """Verantwortlich für die Wiedergabeschleife der Videos."""

    def __init__(self):
        self.driver_manager = WebDriverManager()

    def start(self):
        try:
            driver = self.driver_manager.get_driver()
            for video_url in VIDEO_URLS:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])

                video_player = VideoPlayer(driver)
                video_player.play_video(video_url)

                behavior_simulator = UserBehaviorSimulator(driver)
                behavior_simulator.simulate()

        except Exception as e:
            logging.error(f"Ein Fehler ist aufgetreten: {e}")

        finally:
            self.driver_manager.quit()


def main():
    """Hauptfunktion zur Ausführung der Videoschleife."""
    playback_loop = VideoPlaybackLoop()

    try:
        while True:
            playback_loop.start()
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        logging.info("Schleife durch Benutzer unterbrochen. Beende.")


if __name__ == "__main__":
    main()
