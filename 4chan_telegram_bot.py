import requests
import time

# Telegram configurations items the token and chat id
TELEGRAM_BOT_TOKEN = "BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "CHAT_ID_HERE"

# Keywords to monitor
KEYWORDS = ["words"]

# 4chan API configuration
BOARDS = ["boards"]  # List of 4chan boards to monitor

def send_telegram_alert(message):
    """
    Send an alert message to a Telegram chat.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Failed to send Telegram alert: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")

def check_4chan_for_keywords():
    """
    Check 4chan boards for specific keywords.
    """
    for board in BOARDS:
        print(f"Checking /{board}/ for keywords...")
        try:
            # Get thread list
            threads_url = f"https://a.4cdn.org/{board}/threads.json"
            response = requests.get(threads_url)
            if response.status_code != 200:
                print(f"Failed to fetch threads for /{board}/: {response.status_code}")
                continue

            thread_data = response.json()

            # Iterate through each thread
            for page in thread_data:
                for thread in page['threads']:
                    thread_id = thread['no']
                    posts_url = f"https://a.4cdn.org/{board}/thread/{thread_id}.json"
                    posts_response = requests.get(posts_url)
                    if posts_response.status_code != 200:
                        continue

                    posts_data = posts_response.json()

                    # Check each post in the thread
                    for post in posts_data['posts']:
                        content = post.get('com', '')  # 'com' is the comment key
                        if any(keyword.lower() in content.lower() for keyword in KEYWORDS):
                            alert_message = (
                                f"🚨 Keyword found on /{board}/!\n"
                                f"Thread: https://boards.4chan.org/{board}/thread/{thread_id}\n"
                                f"Content: {content}"
                            )
                            print(alert_message)
                            send_telegram_alert(alert_message)
                            time.sleep(1)  # Prevent spamming alerts
        except Exception as e:
            print(f"Error checking /{board}/: {e}")


if __name__ == "__main__":
    print("Running 4chan keyword monitoring bot...")
    check_4chan_for_keywords()
