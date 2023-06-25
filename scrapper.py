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

    # give the required url here
    url = 'https://www.google.com/search?q=pashupatinath&tbm=isch&ved=2ahUKEwjn8peFmdv_AhXNyKACHUCVDRkQ2-cCegQIABAA&oq=pashupatinath&gs_lcp=CgNpbWcQDFAAWABgAGgAcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1n&sclient=img&ei=94GWZKebK82Rg8UPwKq2yAE&bih=796&biw=1440&rlz=1C5CHFA_enNP1032NP1032'

    wd.get(url)

    image_urls = []
    while len(image_urls) < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd') 
        
        # inspect google image page and find classname of thumbnail and put it in place of 'Q4LuWd'

        for thumbnail in thumbnails[len(image_urls):max_images]:
            try:
                thumbnail.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, 'r48jcc.pT0Scc.iPVvYb') 
            
            # after you click the thumbnail, image opens in google image in right side, inspect that and find classname and put here, 'r48jcc.pT0Scc.iPVvYb'

            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    url = image.get_attribute('src')
                    print(f'Found: {url}')
                    download_image('./images/', url, f'image{len(image_urls)+1}.jpg')
                    image_urls.append(url)

        scroll_down()

    return image_urls


def download_image(download_path, url, filename):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + filename

        with open(file_path, 'wb') as f:
            image.save(f, 'JPEG')

        print('Success')

    except Exception as e:
        print('Failed -', e)


# Specify the path to the WebDriver executable
webdriver_path = '/Users/nirajanpaudel17/Documents/Python/Major-Project/chromedriver'  # Replace with the actual path

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run WebDriver in headless mode (no GUI)
wd = webdriver.Chrome(executable_path=webdriver_path, options=options)

# Scrape images and download
urls = get_images_from_google(wd, 3, 100)

# Quit WebDriver
wd.quit()
