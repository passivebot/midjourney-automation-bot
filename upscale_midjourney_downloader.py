import os
import random
import re
import requests
import shutil
import time
import uuid

from playwright.sync_api import sync_playwright
import eel
import openai

# Set OpenAI API key.
openai.api_key = os.getenv("OPENAI_API_KEY")


@eel.expose
def download_upscaled_images(page, prompt_text):
    try:
        messages = page.query_selector_all(".messageListItem-ZZ7v6g")
        last_four_messages = messages[-4:]
        for message in last_four_messages:
            message_text = message.evaluate_handle('(node) => node.innerText')
            message_text = str(message_text)
            print(message_text)
        if 'Make Variations' in message_text and 'Web' in message_text:
            try:
                last_image = page.query_selector_all('.originalLink-Azwuo9')[-1]
                second_last_image = page.query_selector_all('.originalLink-Azwuo9')[-2]
                third_last_image = page.query_selector_all('.originalLink-Azwuo9')[-3]
                fourth_last_image = page.query_selector_all('.originalLink-Azwuo9')[-4]

                for image in [last_image, second_last_image, third_last_image, fourth_last_image]:
                    src = image.get_attribute('href')
                    url = src
                    response = re.sub(r'[^a-zA-Z0-9\s]', '', prompt_text)
                    response = response.replace(',', '_').replace(' ', '_')
                    response = response[:50]
                    r = requests.get(url, stream=True)
                    with open(f'{str(response) + str(uuid.uuid1())}.png', 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                    del r
            except Exception as e:
                print(f"An error occurred while downloading the images: {e}")
        else:
            download_upscaled_images(page, prompt_text)
    except Exception as e:
        print(f"An error occurred while finding the last message: {e}")


@eel.expose
def generate_prompt_and_submit_command(page, prompt):
    try:
        prompt_text = gpt3_midjourney_prompt(prompt)
        time.sleep(random.randint(1, 5))
        pill_value = page.locator('xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]')
        pill_value.fill(prompt_text)
        time.sleep(random.randint(1, 5))
        page.keyboard.press("Enter")
        print(f'Successfully submitted prompt: {prompt_text}')
        wait_and_select_upscale_options(page, prompt_text)
    except Exception as e:
        print(f"An error occurred while submitting the prompt: {e}")


@eel.expose
def gpt3_midjourney_prompt(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0):
    try:
        if not prompt:
            raise ValueError("Prompt cannot be empty.")
        prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
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


@eel.expose
def get_last_message(page):
    messages = page.query_selector_all(".messageListItem-ZZ7v6g")
    last_message = messages[-1]
    last_message_text = last_message.evaluate_handle('(node) => node.innerText')
    last_message_text = str(last_message_text)
    print(last_message_text)
    return last_message_text


@eel.expose
def main(bot_command, channel_url, PROMPT):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.discord.com/login")
        with open("credentials.txt", "r") as f:
            email = f.readline()
            password = f.readline()
        page.fill("input[name='email']", email)
        time.sleep(random.randint(1, 5))
        page.fill("input[name='password']", password)
        time.sleep(random.randint(1, 5))
        page.click("button[type='submit']")
        time.sleep(random.randint(5, 10))
        page.wait_for_url("https://discord.com/channels/@me", timeout=15000)
        print("Successfully logged into Discord.")
        time.sleep(random.randint(1, 5))
        for i in range(10):
            open_discord_channel(page, channel_url, bot_command, PROMPT)
            print(f"Iteration {i+1} completed.")


@eel.expose
def open_discord_channel(page, channel_url, bot_command, PROMPT):
    page.goto(f"{channel_url}")
    time.sleep(random.randint(1, 5))
    page.wait_for_load_state("networkidle")
    print("Opened appropriate channel.")
    print("Entering the specified bot command.")
    send_bot_command(page, bot_command, PROMPT)
    return page


@eel.expose
def select_upscale_option(page, option_text):
    page.locator(f"button:has-text('{option_text}')").locator("nth=-1").click()
    print(f"Clicked {option_text} upscale option.")


@eel.expose
def send_bot_command(page, command, PROMPT):
    print("Clicking on chat bar.")
    chat_bar = page.locator('xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div')
    time.sleep(random.randint(1, 5))
    print("Typing in bot command")
    chat_bar.fill(command)
    time.sleep(random.randint(1, 5))
    print("Selecting the prompt option in the suggestions menu")
    prompt_option = page.locator('xpath=/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[2]/div/div/div[2]/div[1]/div/div/div')
    time.sleep(random.randint(1, 5))
    prompt_option.click()
    print("Generating prompt using OpenAI's API.")
    generate_prompt_and_submit_command(page, PROMPT)


@eel.expose
def start_bot(art_type, bot_command, channel_url, descriptors, topic):
    PROMPT = f"Generate a Midjourney prompt to result in an {art_type} image about {topic} include {descriptors}"
    print(f"Prompt: {PROMPT}")

    main(bot_command, channel_url, PROMPT)


@eel.expose
def wait_and_select_upscale_options(page, prompt_text):
    prompt_text = prompt_text.lower()
    try:
        last_message = get_last_message(page)
        if 'U1' in last_message:
            print("Found upscale options.")
            print("Attempting to upscale all generated images.")
            try:
                select_upscale_option(page, 'U1')
                time.sleep(random.randint(3, 5))
                select_upscale_option(page, 'U2')
                time.sleep(random.randint(3, 5))
                select_upscale_option(page, 'U3')
                time.sleep(random.randint(3, 5))
                select_upscale_option(page, 'U4')
                time.sleep(random.randint(3, 5))
            except Exception as e:
                print("An error occurred while selecting upscale options:", e)
            download_upscaled_images(page, prompt_text)
        else:
            print("Photo(s) not fully loaded.")
            wait_and_select_upscale_options(page, prompt_text)
    except Exception as e:
        print("An error occurred while finding the last message:", e)


# Initialize eel with your web files folder
eel.init('web')

# Keep this at the bottom, it will start the web server.
eel.start('index.html', mode='chrome', cmdline_args=['--kiosk'])
