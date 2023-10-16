import time
import io
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import Tk, Entry, Button, filedialog, Label, ttk
from tkinter import messagebox
import threading
from selenium.webdriver.chrome.service import Service








progress_bar = None  # Variable to hold the progress bar widget
download_path = None  # Variable to hold the download directory path
webdriver_path = None  # Variable to hold the path to the WebDriver executable
wd = None  # Variable to hold the WebDriver instance

def get_images_from_google(wd, delay, max_images, progress_bar, num_images_label):
    print('get images from google called')
    def scroll_down():
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)

    url = url_entry.get()  # Get the URL from the input box
    print(' Getting the URL from the input box')

    wd.get(url)

    image_urls = set()
    print(image_urls)
    while len(image_urls) < max_images:  # Use len(image_urls) to check the count
        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')
        print('thumbnails')

        for thumbnail in thumbnails:
            try:
                thumbnail.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, 'rg_i')
            print('images called')
            print(images)

            for image in images:
                print('loop called')
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    url = image.get_attribute('src')
                    print(f'Found: {url}')

                    try:
                        print('downloading image')
                        download_image(download_path, url, f'image{len(image_urls) + 1}.jpg', timeout=10)
                        image_urls.add(url)
                        update_progress_bar(progress_bar, len(image_urls), max_images)
                        update_num_images_label(num_images_label, len(image_urls), max_images)
                    except TimeoutError:
                        print(f'Skipped: {url} (Timeout)')

        print('loop finished')
        scroll_down()

    progress_bar.destroy()  # Destroy the progress bar after the download is complete
    print(image_urls)

    return image_urls



def download_image(download_path, url, filename, timeout):
    print('download image called')
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


def open_file_dialog():
    global download_path
    directory = filedialog.askdirectory()  # Show file dialog to select download directory
    download_path = directory + '/'


def select_webdriver():
    global webdriver_path
    global wd
    webdriver_path = filedialog.askopenfilename()  # Show file dialog to select WebDriver executable
    service = Service(webdriver_path)
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Run WebDriver in headless mode
    wd = webdriver.Chrome(service=service, options=options)


def update_progress_bar(progress_bar, current_value, max_value):
    progress = (current_value / max_value) * 100
    progress_bar['value'] = progress
    window.update_idletasks()


def update_num_images_label(label, current_value, max_value):
    label.config(text=f"Downloaded: {current_value}/{max_value}")


def start_download():
    print('start download called')
    global download_path
    global wd
    global progress_bar

    # Check if download directory is selected
    if not download_path:
        window.after(0, lambda: messagebox.showerror("Error", "Please select the download directory."))
        return

    # Check if WebDriver is selected
    if not webdriver_path:
        window.after(0, lambda: messagebox.showerror("Error", "Please select the WebDriver executable."))
        return

    # Get user inputs
    num_images = int(num_images_entry.get())

    # Create progress bar if not already created
    if progress_bar is None:
        progress_bar = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
        progress_bar.pack()

    # Create label for number of images
    num_images_label = Label(window, text="Downloaded: 0/0")
    num_images_label.pack()

    # Update the number of images label
    num_images_label.config(text=f"Downloaded: 0/{num_images}")

    # Start download in a separate thread
    threading.Thread(target=get_images_from_google, args=(wd, 0.1, num_images, progress_bar, num_images_label)).start()


# Create the GUI window
window = Tk()
window.title("Image Downloader")
window.geometry('500x500')  # Set the window size

# URL input box
url_label = Label(window, text="URL:")
url_label.pack()
url_entry = Entry(window, width=100)
url_entry.pack()

# Number of images input box
num_images_label = Label(window, text="Number of Images:")
num_images_label.pack()
num_images_entry = Entry(window)
num_images_entry.pack()

# Button to open file dialog for selecting download directory
file_dialog_button = Button(window, text="Select Directory", command=open_file_dialog)
file_dialog_button.pack()

# Button to open file dialog for selecting WebDriver
webdriver_button = Button(window, text="Select WebDriver", command=select_webdriver)
webdriver_button.pack()

# Button to start download
download_button = Button(window, text="Start Download", command=start_download)
download_button.pack()

# Start the GUI event loop
window.mainloop()
