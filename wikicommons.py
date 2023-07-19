import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_image_sources(html_url, num_images, output_file):
    try:
        # Set up the ChromeOptions to run the webdriver in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        # Initialize the Selenium WebDriver (Chrome) and open the page
        driver = webdriver.Chrome('/Users/nirajanpaudel17/Downloads/chromedriver_mac_arm64/chromedriver', options=chrome_options)
        driver.get(html_url)

        print("Fetching the HTML page...")

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        print("Page loaded. Scrolling to extract image sources...")

        # Scroll to the end of the page multiple times until reaching the expected number of image sources
        scroll_count = 0
        max_attempts = 3  # Set a maximum number of attempts to find and click the "Load more" button
        attempts = 0
        proceed_with_scrolling = True
        image_sources = []

        while scroll_count < num_images and attempts < max_attempts and proceed_with_scrolling:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the new content to load (you can adjust this if needed)
            scroll_count = len(driver.find_elements_by_tag_name("img"))

            # Check if the "Load more" button exists and click it if found
            try:
                load_more_button = driver.find_element(By.CLASS_NAME, "sdms-load-more")
                if load_more_button:
                    load_more_button.click()
                    time.sleep(5)  # Wait for 5 seconds after clicking "Load more" button
                    attempts += 1
            except:
                proceed_with_scrolling = False

            # Wait for the page to stabilize after each scroll and load more content
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

            # Get the HTML content after each scroll and extract the new image sources
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            new_image_sources = [img['src'] for img in soup.find_all('img', src=True)]

            # Filter out duplicate image sources
            new_image_sources = list(set(new_image_sources))

            # Add new image sources to the existing list
            image_sources.extend(new_image_sources)

        # Save the image sources to the specified output file
        with open(output_file, 'w') as f:
            for source in image_sources[:num_images]:
                f.write(source + '\n')

        print(f"{len(image_sources[:num_images])} image sources extracted and saved to '{output_file}'.")

        # Close the WebDriver
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'your_html_page_url' with the URL of the HTML page you want to extract images from
    html_page_url = 'https://commons.wikimedia.org/w/index.php?search=Boudhanath&title=Special:MediaSearch&type=image'

    # Specify the number of image sources you want to extract
    num_images_to_extract = 2000

    # Replace 'output_file.txt' with the desired output file name and path
    output_file_path = '/Users/nirajanpaudel17/Documents/Python/Major-Project/Web-Scrapping/image-sources.txt'

    # Extract image sources from the HTML page and save them to the specified output file
    extract_image_sources(html_page_url, num_images_to_extract, output_file_path)
