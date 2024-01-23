import re
import requests
import toml
import logging
from rich.logging import RichHandler
import telebot

# Logging
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

def load_config(file_path="config.toml"):
    try:
        config = toml.load(file_path)
        telegram_token = config["telegram"]["token"]
        proxy_url = config["web"]["proxy_url"]

        return telegram_token, proxy_url

    except Exception as e:
        log.error(f"Error loading config: {e}")
        return None, None, None

telegram_token, proxy_url = load_config()

log.info(f"Loaded Token: {telegram_token}")
log.info(f"Loaded Proxy URL: {proxy_url}")

# Initialize the Telegram bot
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send me an identifier")
    log.info(f"Received message: {message.text}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Checking: {message.text}")
    log.info(f"Checking: {message.text}")

    # Extract identifier from the message
    email = message.text.strip()

    # Function to extract authenticity token from source
    def extract_auth_token(source):
        log.info("Extracting AUTH Token...")
        left_delim = '<input type="hidden" name="authenticity_token" value="'
        right_delim = '">'
        match = re.search(f"{left_delim}(.*?){right_delim}", source)
        if match:
            return match.group(1)
        return None

    # Function to make the POST request and extract email and phone
    def make_post_request(target_url, proxy_url, email, headers, cookies):
        proxies = {"http": proxy_url, "https": proxy_url}
        post_data = {"authenticity_token": "", "account_identifier": email}

        response = requests.get(target_url, proxies=proxies, headers=headers, cookies=cookies)
        if response.status_code == 200:
            auth_token = extract_auth_token(response.text)
            if auth_token:
                post_data["authenticity_token"] = auth_token
                log.info(f"AUTH Token Fetched: {auth_token}")
                post_response = requests.post(target_url, data=post_data, proxies=proxies, headers=headers, cookies=cookies)

                if "How do you want to reset your password?" in post_response.text:
                    email_left_delim = 'Send an email to <strong dir="ltr">'
                    email_right_delim = '</'
                    phone_left_delim = 'Text a code to the phone number ending in <strong dir="ltr">'
                    phone_right_delim = '</'

                    email_match = re.search(f"{email_left_delim}(.*?){email_right_delim}", post_response.text)
                    phone_match = re.search(f"{phone_left_delim}(.*?){phone_right_delim}", post_response.text)

                    if email_match and phone_match:
                        faemail = email_match.group(1).strip()
                        faphone = phone_match.group(1).strip()

                        log.info(f"Identifier: {email}")
                        log.info(f"Mail Hint: {faemail}")
                        log.info(f"Mobile Hint: {faphone}")
                        bot.reply_to(message, "Identifier: " + email + "\nMail Hint: " + faemail + "\nMobile Hint: " + faphone) 
                elif "Verify your personal information" in post_response.text:
                    log.warning("Further verification needed.")
                elif "Please try again later." in post_response.text:
                    log.warning("Ratelimited / Name banned.")
                elif "We couldn't find your account with that information" in post_response.text:
                    log.error("[No account exists with that Identifier.")
                else:
                    log.error("Error")
        return True

    # Perform the check with the extracted identifier
    target_url = "https://twitter.com/account/begin_password_reset"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Initial GET request to fetch cookies
    response = requests.get(target_url, proxies={"http": proxy_url, "https": proxy_url}, headers=headers)
    if response.status_code == 200:
        cookies = response.cookies
    else:
        log.error(f"Failed to fetch cookies. Status code: {response.status_code}")
        exit()

    success = make_post_request(target_url, proxy_url, email, headers, cookies)

    if success:
        log.info(f"Identifier checked: {email}")

# Start the Telegram bot
bot.polling()