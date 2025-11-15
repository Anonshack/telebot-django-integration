import requests

BASE_URL = "http://127.0.0.1:9222/api/"

FEEDBACKS_ENDPOINT = "feedbacks/"
USERS_ENDPOINT = "users/"

def get_feedbacks(limit=5):
    url = BASE_URL + FEEDBACKS_ENDPOINT
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            print("Currently there are no feedbacks!")
            return

        for fb in data[:limit]:
            print(f"ID: {fb['id']}")
            print(f"User: {fb['user_info']['name']} (@{fb['user_info']['username']})")
            print(f"Text: {fb['text']}")
            print(f"Created At: {fb['created_at']}")
            print("-"*40)

    except requests.exceptions.RequestException as e:
        print("Error working with api!", e)


def get_users(limit=5):
    url = BASE_URL + USERS_ENDPOINT
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            print("There are no users!")
            return

        for user in data[:limit]:
            print(f"ID: {user['id']}")
            print(f"Name: {user['name']} (@{user['username']})")
            print(f"User ID: {user['user_id']}")
            print(f"Clean Username: {user['clean_username']}")
            print(f"Full Info: {user['full_info']}")
            print(f"Created At: {user['created_at']}")
            print("-"*40)

    except requests.exceptions.RequestException as e:
        print("Error working with api!", e)


if __name__ == "__main__":
    print("=== FEEDBACKS ===")
    get_feedbacks()
    print("=== USERS ===")
    get_users()
