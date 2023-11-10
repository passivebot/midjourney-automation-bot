import asyncio
import eel
import logging
import openai
import os
import playwright
import random
import re
import requests
import shutil
import time
import uuid
from loguru import logger
from playwright.async_api import async_playwright, Page
from playwright.sync_api import sync_playwright

# Get logger for this file
logger = logging.getLogger(__name__)
# Set logging level to INFO
logger.setLevel(logging.INFO)

# Define a custom log format without %(asctime)s
log_format = logging.Formatter('[%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - [%(process)d:%(thread)d]')

file_handler = logging.FileHandler('midjourney_automation.log', mode='a')  # Create file handler
file_handler.setFormatter(log_format)  # Set log format for file handler
logger.addHandler(file_handler)  # Add file handler to logger

console_handler = logging.StreamHandler()  # Create console handler
console_handler.setFormatter(log_format)  # Set log format for console handler
logger.addHandler(console_handler)  # Add console handler to logger

# Add condition to check if the current log statement is the same as the previous log statement, if so then don't log it
class NoRepeatFilter(logging.Filter):
    """Filter to ignore repeated log messages."""
    def __init__(self, name=''):
        """Initialize the filter.
        Args:
            name (str): Name of the filter.
        """
        super().__init__(name)
        self.last_log = None

    def filter(self, record):
        """Filter out repeated log messages.
        Args:
            record (LogRecord): Log record to be filtered.
        Returns:
            bool: True if log message is not a repeat, False otherwise.
        """

        # Ignore the %(asctime)s field when comparing log messages
        current_log = record.getMessage().split(' - ', 1)[-1]
        if current_log == self.last_log:
            return False
        self.last_log = current_log
        return True

# Create an instance of the NoRepeatFilter and add it to the logger
no_repeat_filter = NoRepeatFilter()
logger.addFilter(no_repeat_filter)

def random_sleep():
    """Sleep for a random amount of time between 1 and 5 seconds."""
    time.sleep(random.randint(1, 5))

def get_openai_api_key_from_file(filepath):
    """Get OpenAI API key from a file.
    Args:
        filepath (str): Path to the file containing the API key.
    Returns:
        str: API key.
    """
    logger.info("Midjourney Automation bot is reading the API key from file: %s", filepath)
    with open(filepath, 'r') as infile:
        api_key = infile.read().strip()
    logger.info("API key successfully read from file.")
    return api_key

def get_openai_api_key_from_env():
    """Get OpenAI API key from the environment variable.
    Returns:
        str: API key.
    """
    logger.info("Midjourney Automation bot is fetching the API key from environment variable.")
    api_key = os.getenv('OPENAI_API_KEY')
    logger.info("API key successfully read from environment variable.")
    return api_key


def get_openai_api_key_from_user():
    """Get OpenAI API key from user input.
    Returns:
        str: API key.
    """
    logger.info("Waiting for user to enter API key for Midjourney Automation bot.")
    api_key = input("Please enter your OpenAI API key for Midjourney Automation bot: ")
    logger.info("API key successfully entered by the user.")
    return api_key


def set_openai_api_key(api_key):
    """Set OpenAI API key in the environment variable.
    Args:
        api_key (str): API key to set.
    """
    logger.info("Midjourney Automation bot is setting API key in environment variable.")
    os.environ['OPENAI_API_KEY'] = api_key
    logger.info("API key successfully set in environment variable.")


def get_openai_api_key():
    """Get OpenAI API key based on user's preference.
    Returns:
        str: API key.
    """
    while True:
        logger.info("Midjourney Automation bot is asking user for method of entering API key.")
        logger.info("Welcome to the Midjourney Automation bot OpenAI API key setup script.")
        logger.info("How would you like to enter your OpenAI API key for Midjourney Automation bot?")
        logger.info("1. From a file")
        logger.info("2. From the environment")
        logger.info("3. From the console")
        logger.info("4. Exit")
        choice = input("Please enter a number: ")
        if choice == '1':
            logger.info("User chose to enter API key for Midjourney Automation bot from a file.")
            filepath = input("Please enter the filepath to your API key file for Midjourney Automation bot: ")
            return get_openai_api_key_from_file(filepath)
        elif choice == '2':
            logger.info("User chose to enter API key for Midjourney Automation bot from the environment.")
            return get_openai_api_key_from_env()
        elif choice == '3':
            logger.info("User chose to enter API key for Midjourney Automation bot from the console.")
            return get_openai_api_key_from_user()
        elif choice == '4':
            logger.info("User chose to exit the Midjourney Automation bot setup.")
            exit()
        else:
            logger.warning("Invalid choice entered by user for Midjourney Automation bot setup. Retrying.")

@eel.expose
async def download_upscaled_images(page, prompt_text: str):
    try:
        messages = await page.query_selector_all(".messageListItem-ZZ7v6g")
        last_four_messages = messages[-4:]
        
        for message in last_four_messages:
            message_text = await message.evaluate_handle('(node) => node.innerText')
            message_text = str(message_text)

        if 'Vary (Strong)' in message_text and 'Web' in message_text:
            try:
                image_elements = await page.query_selector_all('.originalLink-Azwuo9')
                last_four_images = image_elements[-4:]

                for image in last_four_images:
                    src = await image.get_attribute('href')
                    url = src
                    response = re.sub(r'[^a-zA-Z0-9\s]', '', prompt_text)
                    response = response.replace(' ', '_').replace(',', '_')
                    response = re.sub(r'[\<>:"/|?*]', '', response)
                    response = response.replace('\n\n', '_')
                    response = response[:50].rstrip('. ')
                    download_response = requests.get(url, stream=True)

                    with open(f'{str(response) + str(uuid.uuid1())}.png', 'wb') as out_file:
                        shutil.copyfileobj(download_response.raw, out_file)
                    del download_response

            except Exception as e:
                logger.info(f"An error occurred while downloading the images: {e}")

        else:
            await download_upscaled_images(page, prompt_text)

    except Exception as e:
        logger.info(f"An error occurred while finding the last message: {e}")

@eel.expose
async def generate_prompt_and_submit_command(page, prompt: str):
    try:
        prompt_text = gpt3_midjourney_prompt(prompt)
        random_sleep()
        pill_value_locator = 'span.optionPillValue-2uxsMp'
        await page.fill(pill_value_locator, prompt_text)
        random_sleep()
        await page.keyboard.press("Enter")
        logger.info(f'Successfully submitted prompt: {prompt_text}')
        await wait_and_select_upscale_options(page, prompt_text)
    except Exception as e:
        logger.error(f"An error occurred while submitting the prompt: {e}")
        raise e


@eel.expose
def gpt3_midjourney_prompt(prompt: str, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0) -> str:
    """
    Function to generate a prompt using the OpenAI GPT-3 model.
    
    Parameters:
    - prompt (str): The initial text to base the generation on.
    - engine (str): The id of the engine to use for completion.
    - temp (float): Controls randomness. Lower value means less random.
    - top_p (float): Nucleus sampling. Higher value means more random.
    - tokens (int): The maximum number of tokens to generate.
    - freq_pen (float): Alters the likelihood of choosing tokens based on their frequency.
    - pres_pen (float): Alters the likelihood of choosing tokens based on their presence in the prompt.
    
    Returns:
    - str: The generated text.
    """
    if not prompt:
        logger.error("Prompt cannot be empty.")
        raise ValueError("Prompt cannot be empty.")
    
    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
    
    try:
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
            logger.error("No response from OpenAI API.")
            raise ValueError("No response from OpenAI API.")
        
        text = response.choices[0].text.strip()
        
        if not text:
            logger.error("Response text cannot be empty.")
            raise ValueError("Response text cannot be empty.")
        
        return text
    
    except Exception as e:
        logger.error(f"Error occurred: {e} while generating prompt.")
        raise e

@eel.expose
async def get_last_message(page) -> str:
    """
    Function to get the last message from the provided page.

    Parameters:
    - page: The page from which to fetch the last message.

    Returns:
    - str: The text of the last message.
    """
    try:
        messages = await page.query_selector_all(".messageListItem-ZZ7v6g")
        if not messages:
            logger.error("No messages found on the page.")
            raise ValueError("No messages found on the page.")
        
        last_message = messages[-1]
        last_message_text = await last_message.evaluate('(node) => node.innerText')

        if not last_message_text:
            logger.error("Last message text cannot be empty.")
            raise ValueError("Last message text cannot be empty.")
        
        last_message_text = str(last_message_text)
        # Commented out for now, as it's not needed.
        # logger.info(f"Last message: {last_message_text}")
        return last_message_text
    
    except Exception as e:
        logger.error(f"Error occurred: {e} while getting the last message.")
        raise e


@eel.expose
async def main(bot_command: str, channel_url: str, PROMPT: str):
    """
    Main function that starts the bot and interacts with the page.

    Parameters:
    - bot_command (str): The command for the bot to execute.
    - channel_url (str): The URL of the channel where the bot should operate.
    - PROMPT (str): The prompt text.

    Returns:
    - None
    """
    try:
        browser = None
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.discord.com/login")

            # Get credentials securely
            with open("credentials.txt", "r") as f:
                email = f.readline()
                password = f.readline()
            if not email or not password:
                logger.error("Email or password not provided in credentials.txt.")
                raise ValueError("Email or password not provided in credentials.txt.")
            
            await page.fill("input[name='email']", email)
            await asyncio.sleep(random.randint(1, 5))
            await page.fill("input[name='password']", password)
            await asyncio.sleep(random.randint(1, 5))
            await page.click("button[type='submit']")
            await asyncio.sleep(random.randint(5, 10))
            await page.wait_for_url("https://discord.com/channels/@me", timeout=15000)
            logger.info("Successfully logged into Discord.")
            await asyncio.sleep(random.randint(1, 5))

            for i in range(10):
                await open_discord_channel(page, channel_url, bot_command, PROMPT)
                logger.info(f"Iteration {i+1} completed.")
    except Exception as e:
        logger.error(f"Error occurred: {e} while executing the main function.")
        raise e
    finally:
        if browser:
            await browser.close()

@eel.expose
async def open_discord_channel(page, channel_url: str, bot_command: str, PROMPT: str):
    """
    Function to open a Discord channel and send a bot command.

    Parameters:
    - page: The page object representing the current browser context.
    - channel_url (str): The URL of the channel to open.
    - bot_command (str): The bot command to send.
    - PROMPT (str): The prompt text.

    Returns:
    - None
    """
    try:
        await page.goto(f"{channel_url}")
        await asyncio.sleep(random.randint(1, 5))
        await page.wait_for_load_state("networkidle")
        logger.info("Successfully opened the appropriate channel.")

        logger.info("Entering the specified bot command.")
        await send_bot_command(page, bot_command, PROMPT)
    
    except Exception as e:
        logger.error(f"An error occurred while opening the channel and entering the bot command: {e}")
        raise e

@eel.expose
async def select_upscale_option(page, option_text: str):
    """
    Function to select an upscale option based on the provided text.

    Parameters:
    - page: The page object representing the current browser context.
    - option_text (str): The text of the upscale option to select.

    Returns:
    - None
    """
    try:
        upscale_option = page.locator(f"button:has-text('{option_text}')").locator("nth=-1")
        if not upscale_option:
            logger.error(f"No upscale option found with text: {option_text}.")
            raise ValueError(f"No upscale option found with text: {option_text}.")
        
        await upscale_option.click()
        logger.info(f"Successfully clicked {option_text} upscale option.")
    
    except Exception as e:
        logger.error(f"An error occurred while selecting the upscale option: {e}")
        raise e

@eel.expose
async def send_bot_command(page, command: str, PROMPT: str):
    """
    Function to send a command to the bot in the chat bar.

    Parameters:
    - page: The page object representing the current browser context.
    - command (str): The command to send to the bot.
    - PROMPT (str): The prompt for the command.

    Returns:
    - None
    """
    try:
        logger.info("Clicking on chat bar.")
        chat_bar = page.get_by_role('textbox', name='Message #general')
        await asyncio.sleep(random.randint(1, 5))

        logger.info("Typing in bot command")
        await chat_bar.fill(command)
        #await chat_bar.fill(command)
        await asyncio.sleep(random.randint(1, 5))

        logger.info("Selecting the prompt option in the suggestions menu")
        prompt_option_selector = "#autocomplete-0 > .base-2v-uc0"
        await page.wait_for_selector(prompt_option_selector, state='visible', timeout=10000)
        prompt_option = page.locator(prompt_option_selector)
        await asyncio.sleep(random.randint(1, 5))
        await prompt_option.click()


        logger.info("Generating prompt using OpenAI's API.")
        await generate_prompt_and_submit_command(page, PROMPT)

    except Exception as e:
        logger.exception(f"An error occurred while sending the bot command: {e}")
        raise e

@eel.expose
def start_bot(art_type: str, bot_command: str, channel_url: str, descriptors: str, topic: str):
    """
    Function to start the bot with the specified parameters.

    Parameters:
    - art_type (str): The type of art to generate.
    - bot_command (str): The command to send to the bot.
    - channel_url (str): The URL of the channel where the bot is located.
    - descriptors (str): The descriptors to include in the prompt.
    - topic (str): The topic of the image to generate.

    Returns:
    - None
    """
    try:
        PROMPT = f"Generate a Midjourney prompt to result in an {art_type} image about {topic} include {descriptors}"
        logger.info(f"Prompt: {PROMPT}")

        asyncio.run(main(bot_command, channel_url, PROMPT))

    except Exception as e:
        logger.error(f"An error occurred while starting the bot: {e}")
        raise e

@eel.expose
async def wait_and_select_upscale_options(page, prompt_text: str):
    """
    Function to wait for and select upscale options.

    Parameters:
    - page: The page to operate on.
    - prompt_text (str): The text of the prompt.

    Returns:
    - None
    """
    try:
        prompt_text = prompt_text.lower()

        # Repeat until upscale options are found
        while True:
            last_message = await get_last_message(page)

            # Check for 'U1' in the last message
            if 'U1' in last_message:
                logger.info("Found upscale options. Attempting to upscale all generated images.")
                try:
                    await select_upscale_option(page, 'U1')
                    time.sleep(random.randint(3, 5))
                    await select_upscale_option(page, 'U2')
                    time.sleep(random.randint(3, 5))
                    await select_upscale_option(page, 'U3')
                    time.sleep(random.randint(3, 5))
                    await select_upscale_option(page, 'U4')
                    time.sleep(random.randint(3, 5))
                except Exception as e:
                    logger.error(f"An error occurred while selecting upscale options: {e}")
                    raise e

                await download_upscaled_images(page, prompt_text)
                break  # Exit the loop when upscale options have been found and selected

            else:
                logger.info("Upscale options not yet available, waiting...")
                time.sleep(random.randint(3, 5))

    except Exception as e:
        logger.error(f"An error occurred while finding the last message: {e}")
        raise e

def check_api_key(api_key: str) -> str:
    """
    Function to check if the OpenAI API key is already set, if not, it prompts the user to set it.

    Parameters:
    - api_key (str): The OpenAI API key.

    Returns:
    - str: The OpenAI API key.
    """
    try:
        if api_key:
            logger.info("OpenAI API key for Midjourney Automation bot is already set in the environment.")
        else:
            logger.info("OpenAI API key for Midjourney Automation bot is not set in the environment. Asking user to set it.")
            api_key = get_openai_api_key()

            # You might want to not log the full API key for security reasons.
            logger.info("Your OpenAI API key for Midjourney Automation bot is set.")

            set_openai_api_key(api_key)
            logger.info("Your OpenAI API key for Midjourney Automation bot has been set in the environment.")
        
        return api_key
    except Exception as e:
        logger.error(f"An error occurred while checking or setting the OpenAI API key: {e}")
        raise e

def initialize_bot(api_key: str):
    """
    Function to initialize the bot.

    Parameters:
    - api_key (str): The OpenAI API key.

    This function initializes the web interface with Eel and starts the web server.
    """
    try:
        if not api_key:
            logger.error("API key not provided.")
            raise ValueError("API key not provided.")
        
        # Initialize eel with your web files folder
        eel.init('web')
        logger.info("Eel initialized with web files.")

        # Start the web server.
        eel.start('index.html', mode='chrome', cmdline_args=['--kiosk'])
        logger.info("Web server started.")

    except Exception as e:
        logger.error(f"An error occurred while initializing the bot: {e}")
        raise e
    
if __name__ == '__main__':
    api_key = os.environ.get("OPENAI_API_KEY")
    api_key = check_api_key(api_key)
    initialize_bot(api_key)
