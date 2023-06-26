import time
import io
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_images_from_google(wd, delay, max_images):
    def scroll_down():
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)

    url = input("Enter the Google Images URL: ")

    wd.get(url)

    image_urls = []
    while len(image_urls) < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for thumbnail in thumbnails[len(image_urls):max_images]:
            try:
                thumbnail.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, 'r48jcc.pT0Scc.iPVvYb')

            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    url = image.get_attribute('src')
                    print(f'Found: {url}')

                    try:
                        download_image(download_folder, url, f'image{len(image_urls)+1}.jpg', timeout=10)
                        image_urls.append(url)
                    except TimeoutError:
                        print(f'Skipped: {url} (Timeout)')

        scroll_down()

    return image_urls


def download_image(download_path, url, filename, timeout):
    try:
        image_content = requests.get(url, timeout=timeout).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + filename

        with open(file_path, 'wb') as f:
            image.save(f, 'JPEG')

        print('Success')

    except requests.exceptions.Timeout:
        raise TimeoutError('Download timeout')

    except Exception as e:
        print(f'Failed - {e}')


# User input for URL, download folder, number of images, and delay time
google_images_url = input("Enter the Google Images URL: ")
download_folder = input("Enter the download folder path: ")
num_images = int(input("Enter the number of images to scrape: "))
delay_time = int(input("Enter the delay time in SECONDS: "))
webdriver_path = input("Enter the ChromeDriver executable path: ")

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run WebDriver in headless mode
wd = webdriver.Chrome(executable_path=webdriver_path, options=options)

# Scrape images and download
urls = get_images_from_google(wd, delay_time, num_images)

# Quit WebDriver
wd.quit()
