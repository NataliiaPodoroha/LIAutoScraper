import logging
import sys
import random
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import user_agents


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("out.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def random_sleep(base_time=1.0, variability=0.5):
    time.sleep(base_time + random.uniform(-variability, variability))


def login_to_linkedin(username, password):
    try:
        driver.get(
            "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
        )

        try:
            with open("cookies.txt", "r") as f:
                cookies = eval(f.read())
            for cookie in cookies:
                driver.add_cookie(cookie)
            logging.info("Cookies were successfully loaded.")
        except FileNotFoundError:
            logging.info("Cookies file not found. Logging in as new user.")

        random_sleep(1, 0.5)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys(username)
        random_sleep(0.3, 0.1)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys(password)
        random_sleep(0.3, 0.1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click()

        WebDriverWait(driver, 10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        with open("cookies.txt", "w") as f:
            f.write(str(driver.get_cookies()))
        logging.info("Login to LinkedIn successful and cookies saved.")

    except TimeoutException:
        logging.error("Login timed out.")
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")


def get_profile_picture(profile_url):
    try:
        driver.get(profile_url)
        random_sleep(5, 2)

        profile_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".pv-top-card-profile-picture__image--show")
            )
        )
        img_url = profile_img.get_attribute("src")

        logging.info(f"Profile picture URL: {img_url}")
        return img_url

    except TimeoutException:
        logging.error("Profile picture loading timed out.")
    except Exception as e:
        logging.error(f"An error occurred while fetching profile picture: {e}")
        return None


def generate_filename(profile_url):
    username = urlparse(profile_url).path.strip("/").split("/")[-1]
    return f"{username}.jpeg"


def download_image(img_url, profile_url):
    file_path = generate_filename(profile_url)
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            logging.info(f"Image downloaded successfully and saved as {file_path}")
            return file_path
        else:
            logging.error(
                f"Failed to download image. Status code: {response.status_code}"
            )
            return None
    except Exception as e:
        logging.error(f"An error occurred while downloading image: {e}")
        return None


if __name__ == "__main__":
    driver = init_driver()

    # Replace with your LinkedIn login credentials
    username = "e-mail"
    password = "password"

    try:
        login_to_linkedin(username, password)

        # Replace with a valid LinkedIn profile URL you wish to scrape
        profile_url = "https://www.linkedin.com/in/username/"
        img_url = get_profile_picture(profile_url)

        if img_url:
            download_image(img_url, profile_url)
        else:
            logging.error("Failed to retrieve profile picture URL.")
    finally:
        driver.quit()
