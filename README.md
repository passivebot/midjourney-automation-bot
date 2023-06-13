# midjourney-automation-bot
![SOoEiIS](https://user-images.githubusercontent.com/110620707/235405082-01be9472-2e53-4888-a3bb-daca425dbfd3.png)

As seen on [LinkedIn](https://www.linkedin.com/posts/harmindersinghnijjar_sikhism-sikhi-punjab-activity-7058192758297022464-CPs6?utm_source=share&utm_medium=member_desktop) and [YouTube](https://www.youtube.com/watch?v=IJ0jNhrKQ34).


The Midjourney Automation Bot is a highly efficient Python-based automation program designed to generate and download unique images using the Midjourney bot on Discord. The script employs OpenAI’s GPT-3 to construct image prompts and Playwright, a Node.js library to control Chromium, Firefox, and WebKit browsers, to interact with the Discord application in a browser environment.

### Key Features
GPT-3 Prompt Generation: The bot uses GPT-3 to generate prompts based on user-defined specifications, such as art type, topic, and descriptors.

##### Discord Integration: 
Through Playwright, the bot can navigate to the Discord channel URL where the Midjourney bot resides and submit the generated prompts.

##### Image Upscaling: 
Once the images are generated, the bot interacts with the Discord interface to select upscale options, improving the quality of the images.

##### Image Downloading: 
After upscaling, the bot downloads the images, saving them locally with names corresponding to their prompts.

##### Iterative Execution: 
The bot can be configured to run for a specific number of iterations, continuously generating prompts, submitting them, and downloading the images generated in each cycle.

### Usage
To run the bot, the user needs to set their OpenAI API key and populate several constant fields such as ART_TYPE, BOT_COMMAND, CHANNEL_URL, DESCRIPTORS, TOPIC, and PROMPT. The bot also needs user Discord credentials to log in, which are read from a "credentials.txt" file.

### Error Handling
The bot has robust error handling, making it resilient against issues arising during execution, such as empty prompts or responses, difficulties interacting with Discord's UI, and potential issues in image downloading.

The Midjourney Automation Bot, leveraging GPT-3's creative potential and Playwright's browser automation capabilities, offers an efficient and scalable solution to generate and download unique images from the Midjourney bot on Discord.



