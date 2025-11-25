import json
import os

CONFIG_FILE = "config.json"

def save_token(token):
    """Saves the GitLab Personal Access Token to a local file."""
    data = {"gitlab_token": token}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving token: {e}")
        return False

def load_token():
    """Loads the GitLab Personal Access Token from the local file."""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("gitlab_token")
    except Exception as e:
        print(f"Error loading token: {e}")
        return None

def clear_token():
    """Removes the stored token."""
    if os.path.exists(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
            return True
        except Exception as e:
            print(f"Error clearing token: {e}")
            return False
    return True
