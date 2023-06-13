
# Import modules.
import os

# Define functions to get OpenAI API key from file.
def get_openai_api_key_from_file(filepath):
    with open(filepath, 'r') as infile:
        return infile.read().strip()
    
# Define function to get OpenAI API key from environment.
def get_openai_api_key_from_env():
    return os.environ['OPENAI_API_KEY']

# Define function to get OpenAI API key from user input.
def get_openai_api_key_from_user():
    return input("Please enter your OpenAI API key: ")

# Define function to set OpenAI API key in environment.
def set_openai_api_key(api_key):
    # Set the OpenAI API key in the environment variable by using the command line.
    os.environ['OPENAI_API_KEY'] = api_key

# Ask user how they want to enter their OpenAI API key.
def get_openai_api_key():
    # Run an infinite loop until the user enters a valid choice.
    while True:
        # Print the menu.
        print("Welcome to the Quora Automation OpenAI API key setup script.")
        print("How would you like to enter your OpenAI API key?")
        print("1. From a file")
        print("2. From the environment")
        print("3. From the console")
        print("4. Exit")
        choice = input("Please enter a number: ")
        # If the user enters 1, ask them for the filepath to the API key file.
        if choice == '1':
            filepath = input("Please enter the filepath to your API key file: ")
            return get_openai_api_key_from_file(filepath)
        # If the user enters 2, get the API key from the environment.
        elif choice == '2':
            return get_openai_api_key_from_env()
        # If the user enters 3, ask them to enter the API key.
        elif choice == '3':
            return get_openai_api_key_from_user()
        # If the user enters 4, exit the script.
        elif choice == '4':
            exit()
        # If the user enters anything else, ask them to try again. 
        else:
            print("Invalid choice. Please try again.")

# Main program of the script.
if __name__ == '__main__':
    # Check if the environment variable is already set.
    if "OPENAI_API_KEY" in os.environ:
        print("Your OpenAI API key is already set in the environment.")
        print("You can now run the Upscale Midjourney Downloader.")
        exit()
    # If the environment variable is not set, ask the user how they want to enter their OpenAI API key.
    else:
        print("Your OpenAI API key is not set in the environment.")
        print("Let's set it now.")
        api_key = get_openai_api_key()
        print("Your OpenAI API key is: %s" % api_key)
        set_openai_api_key(api_key)
        print("Your OpenAI API key has been set in the environment.")