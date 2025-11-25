import json
import os
from dotenv import load_dotenv, set_key, unset_key

# Load environment variables from .env file
load_dotenv()

ENV_FILE = ".env"
SETTINGS_FILE = "settings.json"
TOKEN_KEY = "GITLAB_TOKEN"
URL_KEY = "GITLAB_URL"

def save_token(token, url="https://gitlab.wethinkco.de"):
    """Saves the GitLab Personal Access Token and URL to the .env file."""
    try:
        # Create .env if it doesn't exist
        if not os.path.exists(ENV_FILE):
            open(ENV_FILE, 'a').close()
            
        set_key(ENV_FILE, TOKEN_KEY, token)
        set_key(ENV_FILE, URL_KEY, url)
        # Reload to ensure immediate availability in current session
        load_dotenv(override=True)
        return True
    except Exception as e:
        print(f"Error saving token: {e}")
        return False

def load_token():
    """Loads the GitLab Personal Access Token and URL from environment variables."""
    token = os.getenv(TOKEN_KEY)
    url = os.getenv(URL_KEY, "https://gitlab.wethinkco.de")
    return token, url

def clear_token():
    """Removes the stored token and URL from .env."""
    try:
        if os.path.exists(ENV_FILE):
            unset_key(ENV_FILE, TOKEN_KEY)
            unset_key(ENV_FILE, URL_KEY)
            # Reload to reflect removal
            load_dotenv(override=True)
        return True
    except Exception as e:
        print(f"Error clearing token: {e}")
        return False

# --- App State Management ---

def save_app_state(key, value):
    """Saves a key-value pair to the settings.json file."""
    data = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading settings file: {e}")
    
    data[key] = value
    
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving app state: {e}")
        return False

def load_app_state(key):
    """Loads a value from the settings.json file by key."""
    if not os.path.exists(SETTINGS_FILE):
        return None
    
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return data.get(key)
    except Exception as e:
        print(f"Error loading app state: {e}")
        return None
