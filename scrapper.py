# import time
# import io
# import requests
# from PIL import Image
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# def get_images_from_google(wd, delay, max_images):
#     def scroll_down():
#         wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
#         time.sleep(delay)

#     # give the required url here
#     url = 'https://www.google.com/search?q=lumbini&tbm=isch&ved=2ahUKEwjwgrzJmt7_AhUsrmMGHZZEDYsQ2-cCegQIABAA&oq=lumbini&gs_lcp=CgNpbWcQDFAAWABgAGgAcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1n&sclient=img&ei=OhaYZPD9IazcjuMPlom12Ag&bih=821&biw=1440&rlz=1C5CHFA_enNP1032NP1032'

#     wd.get(url)

#     image_urls = []
#     while len(image_urls) < max_images:
#         thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd') 
        
#         # inspect google image page and find classname of thumbnail and put it in place of 'Q4LuWd'

#         for thumbnail in thumbnails[len(image_urls):max_images]:
#             try:
#                 thumbnail.click()
#                 time.sleep(delay)
#             except:
#                 continue

#             images = wd.find_elements(By.CLASS_NAME, 'r48jcc.pT0Scc.iPVvYb') 
            
#             # after you click the thumbnail, image opens in google image in right side, inspect that and find classname and put here, 'r48jcc.pT0Scc.iPVvYb'

#             for image in images:
#                 if image.get_attribute('src') and 'http' in image.get_attribute('src'):
#                     url = image.get_attribute('src')
#                     print(f'Found: {url}')
#                     download_image('./images/Lumbini/', url, f'image{len(image_urls)+1}.jpg')
#                     image_urls.append(url)

#         scroll_down()

#     return image_urls


# def download_image(download_path, url, filename):
#     try:
#         image_content = requests.get(url).content
#         image_file = io.BytesIO(image_content)
#         image = Image.open(image_file)
#         file_path = download_path + filename

#         with open(file_path, 'wb') as f:
#             image.save(f, 'JPEG')

#         print('Success')

#     except Exception as e:
#         print('Failed -', e)


# # Specify the path to the WebDriver executable
# webdriver_path = '/Users/nirajanpaudel17/Documents/Python/Major-Project/chromedriver'  # Replace with the actual path

# # Set up WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run WebDriver in headless mode (no GUI)
# wd = webdriver.Chrome(executable_path=webdriver_path, options=options)

# # Scrape images and download
# urls = get_images_from_google(wd, 0.1, 150)

# # Quit WebDriver
# wd.quit()


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

    url = 'https://www.google.com/search?rlz=1C5CHFA_enNP1032NP1032&sxsrf=APwXEdf2hMbCziKF_g_YQHuClE_SMpOxOA:1687690308726&q=patan+durbar+square&tbm=isch&sa=X&ved=2ahUKEwiCqd6qoN7_AhUDV2wGHaFrBRwQ0pQJegQICxAB&biw=1440&bih=821&dpr=2'

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
                        download_image('./Patan-Durbar-Square/', url, f'image{len(image_urls)+1}.jpg', timeout=10)
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


# Specify the path to the WebDriver executable
webdriver_path = '/Users/nirajanpaudel17/Documents/Python/Major-Project/chromedriver'  # Replace with the actual path

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run WebDriver in headless mode
wd = webdriver.Chrome(executable_path=webdriver_path, options=options)

# Scrape images and download
urls = get_images_from_google(wd, 0.1, 150)

# Quit WebDriver
wd.quit()
