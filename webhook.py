import requests
from colorama import Fore, Style

# Initialize colorama
Fore.GREEN = Fore.GREEN
Fore.RED = Fore.RED
Fore.RESET = Style.RESET_ALL

# import webhook via file
def import_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            webhook_urls = [line.strip() for line in file]
        return webhook_urls
    except FileNotFoundError:
        print(Fore.RED + "File not found: " + file_path + Fore.RESET)
        return []

# import webhook urls from copy/paste
def import_from_copybook():
    webhook_urls = []
    while True:
        webhook_url = input("Enter a Discord Webhook URL (or press enter to finish): ")
        if webhook_url == "":
            break
        webhook_urls.append(webhook_url)
    return webhook_urls

# main snippet
choice = input("Choose an option:\n1. Import from file\n2. Import from copybook\nEnter your choice (1 or 2): ")

if choice == "1":
    file_path = r"PATH_TO_YOUR_FILE.txt"  # replace with the actual file path
    webhook_urls = import_from_file(file_path)
elif choice == "2":
    webhook_urls = import_from_copybook()
else:
    print(Fore.RED + "Invalid choice. Exiting the program." + Fore.RESET)
    exit()

if not webhook_urls:
    print(Fore.RED + "No Webhook URLs found. Exiting the program." + Fore.RESET)
    exit()

# input message you want to spam
message = input("Enter the message you want to spam: ")

# spam loop
while True:
    for webhook_url in webhook_urls:
        try:
            # send request to webhook url
            response = requests.post(webhook_url, json={"content": message})
            
            # check request response
            if response.status_code == 204:
                print(Fore.GREEN + "Message sent successfully to " + webhook_url + Fore.RESET)
            elif response.status_code == 429:
                print(Fore.RED + "Rate limit exceeded. Failed to send message to " + webhook_url + Fore.RESET)
            else:
                print(Fore.RED + "Failed to send message to " + webhook_url + ". Status code: " + str(response.status_code) + Fore.RESET)
        except Exception as e:
            print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
            break