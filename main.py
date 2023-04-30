# Description: This script automates the process of answering a question on Quora using GPT-3.
# Author: harmindesinghnijjar
# Date: 2023-04-29
# Version: 1.0.0
# Usage: python main.py

# Import modules.
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import getpass
import openai
import os
import time
import set_openai_api_key
import urllib.request

CHANNEL_URL = ""
COMMAND = "/imagine"
# Set OpenAI API key.
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set username.
user = getpass.getuser()

# Define a Selenium class to automate the browser.
class Selenium(webdriver.Chrome):
    # Constructor method. 
    def __init__(self, webdriverval):
        driver = webdriverval


    # Method to open Discord channel with Midjourney bot.
    def open_channel(self, url):
        try:
            # Open a webpage.
            self.get(url)
        except Exception as e:
            print(f"Error occurred: {e}")
            return None


    # Method to enter bot command into the Discord chat bar.
    def bot_command(self, command):
        try:
            chat_bar = self.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div').click()
        except NoSuchElementException:
            print("Could not find chat bar on the page.")
            return ""
        except Exception as e:
            print("An error occurred while clicking the chat bar:", e)
            return ""
        
        time.sleep(5)
        
        try: 
            chat_bar = chat_bar = self.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div')
            chat_bar.send_keys(COMMAND)
        except Exception as e:
            print(f"An error, {e}, occured while entering {command} into the chat bar.")

        try:
            prompt_div = self.find_element(By.XPATH, '//*[@id="autocomplete-0"]/div')
            prompt_div.click()
        except Exception as e:
            print(f"An error, {e}, occured while clicking on prompt option.")

        try:
            pillValue = self.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]')
            prompt = f"Write a Midjourney image generation prompt about..."
            response = selenium_client.gpt3_midjourney_prompt(prompt)
            print(response)
            pillValue.send_keys(response)
            time.sleep(10)
            pillValue.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"An error, {e}, occured while filling in image description.")
        
        # Wait for the image to generate.
        # time.sleep(60) 

        try:
            # Download the image that the bot responds with.
            last_image = self.find_elements(By.CLASS_NAME, 'originalLink-Azwuo9')[-1]
            time.sleep(5)
            src = last_image.get_attribute('href')
            print(src)
            url = src
            
            r = requests.get(url, stream=True)
            with open ('img.png', 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            del r


            


        except Exception as e:
            print(f"An error, {e}, occured while downloading the image.")

        

        
    # Method to ask GPT-3 the question extracted from Quora and return the respone text as a string.
    def gpt3_midjourney_prompt(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0):
        try:
            if not prompt:
                raise ValueError("Prompt cannot be empty.")
            prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen
            )
            if not response.choices:
                raise ValueError("No response from OpenAI API.")
            text = response.choices[0].text.strip()
            if not text:
                raise ValueError("Response text cannot be empty.")
            return text
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    
    
    # Method to close the Chrome instance.
    def close_browser(driver):
        """
        Closes the web browser.

        Args:
        driver (selenium.webdriver.Chrome): The Chrome web driver object.

        Returns:
        None
        """
        driver.quit()

    # Method to set up the Chrome instance. 
    def setup(self):
        # AttributeError: 'Selenium' object has no attribute 'w3c'
        # Set Chrome window size to maximize.
        self.maximize_window()
        
        # Set implicit wait time to 10 seconds.
        self.implicitly_wait(10)
        
        # Set page load timeout to 20 seconds.
        self.set_page_load_timeout(20)


 
if __name__ == '__main__':
    # Check if the OpenAI API key is set in the environment using the set_openai_api_key module.
    # If it is, then run the script.
        if set_openai_api_key.check_openai_api_key():
            os_command = 'taskkill /im chrome.exe /f'
            os.system(os_command)
            # Create an empty list to store conversation history.
            conversation = list()
            # Define Chrome options.
            options = Options()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # Add a user data directory as an argument for options.
            options.add_argument(f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data")
            options.add_argument("profile-directory=Default")
            # In order to prevent the "Timed out receiving message from renderer: 20.000" error, add the following options.
            options.add_experimental_option('extensionLoadTimeout', 60000)
            # Instansiate Google Chrome with the above options. 
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            selenium_client = Selenium
            selenium_client.setup(driver)
            # Pause for 2 seconds.
            time.sleep(2)
            # Create an infinite loop.
            while True:
                selenium_client.open_channel(driver, CHANNEL_URL)
                # Pause for 5 seconds.
                time.sleep(5)
                selenium_client.bot_command(driver, COMMAND)
                time.sleep(5)
                #selenium_client.quit()
        else:
            print("OpenAI API key not set in environment.")
            # Get the OpenAI API key from the user.
            api_key = set_openai_api_key.get_openai_api_key()
            # Set the OpenAI API key in the environment.
            set_openai_api_key.set_openai_api_key(api_key)
            # Open the environment variables in the Windows GUI with OpenAI API key highlighted.
            set_openai_api_key.open_env()
            # Run the script.

