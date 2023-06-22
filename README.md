# midjourney-automation-bot
![GUI](https://github.com/passivebot/midjourney-automation-bot/blob/8efd67a4e6e09b844db6da809469fbe26e90a60f/chrome_zrfWeRJEmB.png)

As seen on [LinkedIn](https://www.linkedin.com/posts/harmindersinghnijjar_sikhism-sikhi-punjab-activity-7058192758297022464-CPs6?utm_source=share&utm_medium=member_desktop) and [YouTube](https://www.youtube.com/watch?v=IJ0jNhrKQ34).


The Midjourney Automation Bot is a highly efficient Python-based automation program designed to generate and download unique images using the Midjourney bot on Discord. The script employs OpenAI’s GPT-3 to construct image prompts and Playwright, a Node.js library to control Chromium, Firefox, and WebKit browsers, to interact with the Discord application in a browser environment.

### Customization
This program can be customized to your personal/organizational needs. For more information, please contact me via [LinkedIn](https://www.linkedin.com/in/harmindersinghnijjar/) or email at harmindernijjar1996@gmail.com

### Key Features
<b>GPT-3 Prompt Generation:</b> The bot uses GPT-3 to generate prompts based on user-defined specifications, such as art type, topic, and descriptors.

<b>Discord Integration:</b> Through Playwright, the bot can navigate to the Discord channel URL where the Midjourney bot resides and submit the generated prompts.

<b>Image Upscaling:</b> Once the images are generated, the bot interacts with the Discord interface to select upscale options, improving the quality of the images.

<b>Image Downloading:</b> After upscaling, the bot downloads the images, saving them locally with names corresponding to their prompts.

<b>Iterative Execution:</b> The bot can be configured to run for a specific number of iterations, continuously generating prompts, submitting them, and downloading the images generated in each cycle.

### Usage
To run the bot, the user needs to set their OpenAI API key and populate several constant fields such as ART_TYPE, BOT_COMMAND, CHANNEL_URL, DESCRIPTORS, TOPIC, and PROMPT. The bot also needs user Discord credentials to log in, which are read from a "credentials.txt" file.

### Error Handling
The bot has robust error handling, making it resilient against issues arising during execution, such as empty prompts or responses, difficulties interacting with Discord's UI, and potential issues in image downloading.

The Midjourney Automation Bot, leveraging GPT-3's creative potential and Playwright's browser automation capabilities, offers an efficient and scalable solution to generate and download unique images from the Midjourney bot on Discord.



