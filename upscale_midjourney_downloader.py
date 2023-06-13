from playwright.sync_api import expect
from playwright.sync_api import sync_playwright
import openai
import os
import random
import re
import requests
import shutil
import time
import uuid

# Set OpenAI API key.
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants.
ART_TYPE = ""
BOT_COMMAND = "/imagine"
CHANNEL_URL = ""
DESCRIPTORS = ""
TOPIC = ""
PROMPT = f"Generate a Midjourney prompt to result in an {ART_TYPE} image about {TOPIC} include {DESCRIPTORS}"



# If any of the constants are not set, ask it as user input and exit.
if ART_TYPE == "":
    print("Enter art type in line 18 of the source code.")
    exit()
if BOT_COMMAND == "":
    print("Enter bot command in line 19 of the source code.")
    exit()
if CHANNEL_URL == "":
    print("Enter channel URL in line 20 of the source code.")
    exit()
if DESCRIPTORS == "":
    print("Enter descriptors in line 21 of the source code.")
    exit()
if TOPIC == "":
    print("Enter topic in line 22 of the source code.")
    exit()
if PROMPT == "":
   print("Enter prompt to send to OpenAI's API in line 23 of the source code.")
   exit()

# Function to login to Discord.
def open_discord_channel(page):
        # Go to appropriate channel.
        page.goto(f"{CHANNEL_URL}")
        time.sleep(random.randint(1, 5))
        page.wait_for_load_state("networkidle")  # This waits for the "networkidle"
        print("Opened appropriate channel.")
        print("Entering in the specified bot command.")
        bot_command(page, BOT_COMMAND)
        return page
        
# Function to ask GPT-3 for the image prompt.
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
            print(f"Error occurred: {e} while generating prompt.")
            return None

# Function to click all upscale buttons.
def select_upscale_option(page, option_text):    
    # Click the last button on the page that contains the option text.
    page.locator(f"button:has-text('{option_text}')").locator("nth=-1").click()
    print(f"Clicked {option_text} upscale option.")

# Function to download upscaled images.
def download_upscaled_images(page, prompt_text):
    # Wait for all four images to complete rendering by checking the contents of the last 4 messages to see if it
    # contains the phrase 'Make Variations', and 'Web'.
    messages = page.query_selector_all(".messageListItem-ZZ7v6g")
    last_four_messages = messages[-4:]
    # Get the inner text of the last four messages by evaluating the innerText property of the node.
    for message in last_four_messages:
        message = message.evaluate_handle('(node) => node.innerText')
        message = str(message)
        print(message)
    # Check to see if string contains the 'Make Variation' and 'Web'.
    if 'Make Variations' and 'Web' in message:
        try: 
            print('Downloading upscaled images.')
            try:
                # Download last 4 images.
                last_image = page.query_selector_all('.originalLink-Azwuo9')[-1]
                second_last_image = page.query_selector_all('.originalLink-Azwuo9')[-2]
                third_last_image = page.query_selector_all('.originalLink-Azwuo9')[-3]
                fourth_last_image = page.query_selector_all('.originalLink-Azwuo9')[-4]

                # Loop and download all 4 images with the same name as the prompt, along with last_image, second_last_image, etc.
                for image in [last_image, second_last_image, third_last_image, fourth_last_image]:
                    src = image.get_attribute('href')
                    url = src
                    # # Only keep name until first period.
                    # response = re.sub(r'\w+\.', '', response)
                    # Remove all special characters from the response using regex.
                    response = re.sub(r'[^a-zA-Z0-9\s]', '', prompt_text)
                    # Replace all commas and spaces with underscores.
                    response = response.replace(',', '_').replace(' ', '_')   
                    # Get first 200 characters of response.
                    response = response[:200]     
                    r = requests.get(url, stream=True)
                    with open(f'{str(response) + str(uuid.uuid1())}.png', 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                    del r

            except Exception as e:
                print(f"An error, {e}, occured while downloading the images.")
        except Exception as e:
            print(e)
    else:
        # Call the function again.
        download_upscaled_images(page, prompt_text)
        
# Function to get the last message.
def get_last_message(page):
        # Obtain the list of all messages.
        # messageListItem-ZZ7v6g
        messages = page.query_selector_all(".messageListItem-ZZ7v6g")
        # Select the last message.
        last_message = messages[-1]
        # Get the text of the last message.
        last_message = last_message.evaluate_handle('(node) => node.innerText')
        last_message = str(last_message)
        print(last_message)
        return last_message

# Function to wait for page to fully load and select all upscale options.
def wait_and_select_upscale_options(page, prompt_text):
    prompt_text = prompt_text.lower()
    try:
        last_message = get_last_message(page)
        # Check to see if string contains the 'U1'.
        if 'U1' in last_message:
            print("Found upscale options.")
            print("Attempting to upscale all generated images.")
            try: 
                # Select the 'U1' upscale option
                select_upscale_option(page, 'U1')
                time.sleep(random.randint(3, 5))
                # Select the 'U2' upscale option
                select_upscale_option(page, 'U2')
                time.sleep(random.randint(3, 5))
                # Select the 'U3' upscale option
                select_upscale_option(page, 'U3')
                time.sleep(random.randint(3, 5))
                # Select the 'U4' upscale option
                select_upscale_option(page, 'U4')
                time.sleep(random.randint(3, 5))
            except Exception as e:
                print("An error occured while selecting upscale options:", e)
            download_upscaled_images(page, prompt_text)
        else:
            print("Photo(s) not fully loaded.")
            # KNOWN ISSUE: Script will sometimes start monitoring second last message instead of the last one.
            # Keep looping until upscale options are found.
            wait_and_select_upscale_options(page, prompt_text)
    except Exception as e:
        print("An error occurred while finding the last message:", e)
    

# Function to generate prompt and sumbit command.
def generate_prompt_and_submit_command(page, prompt):
    try:
        # Generate prompt.
        prompt_text = gpt3_midjourney_prompt(prompt)
        time.sleep(random.randint(1, 5))
        pill_value = page.locator('xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]')
        pill_value.fill(prompt_text)
        # Submit prompt.
        time.sleep(random.randint(1, 5))
        # Press the Enter key.
        page.keyboard.press("Enter")
        print(f'Successfully submitted prompt: {prompt_text}')
        wait_and_select_upscale_options(page, prompt_text)
    except Exception as e:
        print("An error occurred while submitting the prompt:", e)

# Function to enter in bot command.
def bot_command(page, command):
    try:
        print("Clicking on chat bar.")
        chat_bar = page.locator('xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div')
        time.sleep(random.randint(1, 5))
        print("Typing in bot command")
        chat_bar.fill(command)
        time.sleep(random.randint(1, 5))
        print("Selecting the prompt option in the suggestions menu")
        # Select the first option in the pop-up menu.
        prompt_option = page.locator('xpath=/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[2]/div/div/div[2]/div[1]/div/div/div')
        time.sleep(random.randint(1, 5))
        # Click on the prompt option.
        prompt_option.click()
        print("Generating prompt using OpenAI's API.")
        generate_prompt_and_submit_command(page, PROMPT)
    except Exception as e:
        print("An error occurred while entering in the prompt:", e)

# Main function to login to Discord and run the bot.
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # Create a new incognito browser context.
        page = browser.new_page()
        # Go to Discord login page.
        page.goto("https://www.discord.com/login")
        # Open credentials file and read in email and password.
        with open("credentials.txt", "r") as f:
            email = f.readline()
            password = f.readline()
        # Fill in email and password fields.
        print("Entering email")
        page.fill("input[name='email']", email)
        time.sleep(random.randint(1, 5))
        print("Entering password")
        page.fill("input[name='password']", password)
        time.sleep(random.randint(1, 5))
        # Click login button.
        print("Logging into Discord")
        page.click("button[type='submit']")
        time.sleep(random.randint(5, 10))
        # Wait for page URL to change for 15 seconds.
        page.wait_for_url("https://discord.com/channels/@me", timeout=15000)
        print("Successfully logged into Discord.")
        time.sleep(random.randint(1, 5))
        # Run the bot for 10 iterations.
        for i in range(10):
            open_discord_channel(page)
             # Go to appropriate channel.
            page.goto(f"{CHANNEL_URL}")
            time.sleep(random.randint(1, 5))
            page.wait_for_load_state("networkidle")  # This waits for the "networkidle"
            print("Opened appropriate channel.")
            print("Entering in the specified bot command.")
            bot_command(page, BOT_COMMAND)
            # Print the number of iterations completed.
            print(f"Iteration {i+1} completed.")
  


   

    
    
