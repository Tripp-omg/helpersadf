import requests

WEBHOOK_URL = 'https://discord.com/api/webhooks/1269062586763313247/1rowQkSGkR8VdbE-orCnT0SUHbOjZxm41QOlA_DFl2d0nhgAhvobXlU0pWMwq29NWeSv'  # Replace with your actual webhook URL

def log_to_webhook(message: str):
    """Send a log message to the specified webhook URL."""
    data = {
        "content": message,
        "username": "Rank Bot Logger"  # Optional: Set the username of the webhook
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send log message to webhook: {e}")
