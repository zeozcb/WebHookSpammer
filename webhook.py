import asyncio
import aiohttp
from colorama import Fore, Style
import sys

if sys.platform == 'win32':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# colorama colors
Fore.GREEN = Fore.GREEN
Fore.RED = Fore.RED
Fore.YELLOW = Fore.YELLOW
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

async def send_message(session, webhook_url, message):
    try:
        async with session.post(webhook_url, json={"content": message}) as response:
            if response.status == 204:
                print(Fore.GREEN + "Message sent successfully to " + webhook_url + Fore.RESET)
            elif response.status == 429:
                print(Fore.YELLOW + "Rate limit exceeded. Failed to send message to " + webhook_url + Fore.RESET)
            else:
                print(Fore.RED + "Failed to send message to " + webhook_url + ". Status code: " + str(response.status) + Fore.RESET)
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)

async def main():
    choice = input("Choose an option:\n1. Import from file\n2. Import from copybook\nEnter your choice (1 or 2): ")

    if choice == "1":
        file_path = r"C:\Users\zeo\Desktop\WebHookSpammer\name.txt"  # replace with the actual file path
        webhook_urls = import_from_file(file_path)
    elif choice == "2":
        webhook_urls = import_from_copybook()
    else:
        print(Fore.RED + "Invalid choice. Exiting the program." + Fore.RESET)
        return

    if not webhook_urls:
        print(Fore.RED + "No Webhook URLs found. Exiting the program." + Fore.RESET)
        return

    message = input("Enter the message you want to spam: ")

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for webhook_url in webhook_urls:
                task = asyncio.ensure_future(send_message(session, webhook_url, message))
                tasks.append(task)
            await asyncio.gather(*tasks)
            # Add a delay between each iteration to avoid overloading the server
            await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
