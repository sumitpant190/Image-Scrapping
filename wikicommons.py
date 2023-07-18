import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_image_sources(html_url, num_images):
    try:
        # Initialize the Selenium WebDriver (Chrome) and open the page
        driver = webdriver.Chrome('/Users/nirajanpaudel17/Downloads/chromedriver_mac_arm64/chromedriver')
        driver.get(html_url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        # Scroll to the end of the page to load more content
        scroll_count = 0
        while scroll_count < num_images:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the new content to load (you can adjust this if needed)
            scroll_count = len(driver.find_elements_by_tag_name("img"))

            # Check if the "Load more" button exists and click it if found
            load_more_button = driver.find_element(By.CLASS_NAME, "sdms-load-more")
            if load_more_button:
                load_more_button.click()
                time.sleep(2)  # Wait for the new content to load after clicking "Load more" button

        # Get the HTML content after scrolling
        page_source = driver.page_source

        # Close the WebDriver
        driver.quit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all the image tags and extract their sources
        image_sources = [img['src'] for img in soup.find_all('img', src=True)]

        return image_sources[:num_images]

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    # Replace 'your_html_page_url' with the URL of the HTML page you want to extract images from
    html_page_url = 'https://commons.wikimedia.org/w/index.php?search=Boudhanath&title=Special:MediaSearch&type=image'

    # Specify the number of image sources you want to extract
    num_images_to_extract = 100

    # Extract image sources from the HTML page
    image_sources_list = extract_image_sources(html_page_url, num_images_to_extract)

    # Display the extracted image sources
    print("Image sources:")
    for source in image_sources_list:
        print(source)
