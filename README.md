# Midjourney Automation Bot

![GUI](https://github.com/passivebot/midjourney-automation-bot/blob/8efd67a4e6e09b844db6da809469fbe26e90a60f/chrome_zrfWeRJEmB.png)

The Midjourney Automation Bot is a script that automates image generation using the OpenAI GPT-3 model. It interacts with Discord channels and generates images based on user prompts. This bot can be used to create various types of art, such as illustrations, digital paintings, or sketches.

As seen on [LinkedIn](https://www.linkedin.com/posts/harmindersinghnijjar_sikhism-sikhi-punjab-activity-7058192758297022464-CPs6?utm_source=share&utm_medium=member_desktop) and [YouTube](https://www.youtube.com/watch?v=IJ0jNhrKQ34).

## Contact

For any queries or freelance opportunities, please get in touch with me via [LinkedIn](https://www.linkedin.com/in/harmindersinghnijjar/) or email at harmindernijjar1996@gmail.com

## Table of Contents

- [How it Works](#how-it-works)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Customization](#customization)
- [License](#license)
- [Credits](#credits)

## How it Works

1. The bot logs into Discord using user credentials provided in a secure configuration file.
2. The bot opens the specified channel on Discord.
3. The bot sends a command to generate an image based on the user's prompt.
4. The bot waits for the upscale options to appear and selects them.
5. The bot downloads the upscaled images.

The prompt can include descriptors and a topic to guide the image generation process. The bot uses the OpenAI GPT-3 model to generate the image based on the prompt. The generated images are then downloaded and saved.

## Features

- Logging: The bot logs its actions and any errors during the image generation process.
- API Key Management: The bot allows users to set the OpenAI API key through different methods, such as a file, environment variable, or console input.
- Customizable Upscale Options: The bot selects, and downloads upscaled images based on user-defined upscale options.
- Web Interface: The bot provides a user-friendly web interface powered by Eel, allowing users to interact with and control the bot easily.

## Getting Started

To get started with the Midjourney Automation Bot, follow these steps:

1. Clone the repository: `git clone https://github.com/passivebot/midjourney-automation-bot.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the bot: `python midjourney_automation_script.py`
4. Customize the bot's behavior by modifying the values in the GUI, such as the bot command, channel URL, prompt, etc.
5. Click "Start Automation" to start generating images.

## Usage

Once the bot runs, it will automatically log into Discord, open the specified channel, and send the bot command with the given prompt. The bot will then wait for the upscale options, select them, and download the upscaled images.

You can interact with the bot through the web interface, which you can access by opening `index.html` in your preferred web browser. The web interface allows you to start the bot, configure the bot parameters, and monitor the bot's progress and log messages.

## Customization

The bot is designed with customization in mind. Users can modify various parameters and settings according to their needs. You can set the OpenAI API key, choose the upscale options, decide the Discord channel, and much more. To make these customizations, simply adjust the values in the GUI before starting the bot.

## License

The Midjourney Automation Bot is licensed under the [MIT License](https://github.com/passivebot/midjourney-automation-bot/blob/main/LICENSE).

## Credits

Developed by [Harminder Singh Nijjar](https://github.com/harmindersinghnijjar)





