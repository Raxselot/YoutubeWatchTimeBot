from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

VIDEO_URLS = [
              'https://www.youtube.com/yourvideolink'  #Insert Your Youtube Link here
              ]
WAIT_TIME = 5 
COOKIE_ACCEPT_WAIT = 15  
AD_SKIP_WAIT = 20  


logging.basicConfig(level=logging.INFO)


def setup_driver():
    """Setup and return a Chrome WebDriver instance."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


def handle_cookie_consent(driver):
    """Handle cookie consent"""
    try:
        accept_button = WebDriverWait(driver, COOKIE_ACCEPT_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//button//span[text()='Alle akzeptieren']"))
        )
        driver.execute_script("arguments[0].click();", accept_button)
        logging.info("Cookie consent accepted")
    except Exception as e:
        logging.warning(f"No cookie consent dialog found or error occurred: {e}")


def skip_ads(driver):
    """Skip ads if the skip button is available."""
    while True:
        try:
            ad_skip_button = WebDriverWait(driver, AD_SKIP_WAIT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button"))
            )
            ad_skip_button.click()
            logging.info("Skipped ad")
            time.sleep(1) 
        except Exception as e:
            logging.info(f"No more ads to skip or error occurred: {e}")
            break  


def check_for_video_playing(driver):
    """Check if the main video is playing."""
    check_ad_playing = driver.execute_script("return document.querySelector('.html5-video-player').classList.contains('ad-showing');")
    return not check_ad_playing


def check_if_video_is_paused(driver):
    """Check if the video is currently paused."""
    paused = driver.execute_script("return document.querySelector('video').paused;")
    return paused


def play_video(driver, video_url):
    """Play the video from the given URL."""
    driver.get(video_url)
    
    handle_cookie_consent(driver)
    
    time.sleep(5) 
    
    skip_ads(driver)

    while not check_for_video_playing(driver):
        logging.info("Waiting for main video to start...")
        time.sleep(1)

    if check_if_video_is_paused(driver):
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)  
        logging.info("Video was paused. Now playing.")
    else:
        logging.info("Video is already playing.")

    video_duration = driver.execute_script("return document.querySelector('video').duration;")
    logging.info(f"Video duration: {video_duration} seconds")
    
    stop_time = random.uniform(0.7 * video_duration, video_duration)
    logging.info(f"Video will stop after: {stop_time} seconds")

    time.sleep(video_duration)


def play_video_loop():
    """Loop through the video URLs and play them."""
    driver = setup_driver()

    try:
        for video_url in VIDEO_URLS:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            play_video(driver, video_url)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        driver.quit()


def main():
    """Main function to execute the video loop."""
    try:
        while True:
            play_video_loop()
            time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        logging.info("Loop interrupted by user. Exiting")


if __name__ == "__main__":
    main()
