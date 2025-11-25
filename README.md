# Project_manager


***

# 🦊 GitLab Manager GUI

A modern, desktop-based Graphical User Interface (GUI) for managing GitLab projects, issues, and merge requests. This application uses the GitLab API to provide a streamlined workflow, allowing developers to manage their board without constantly switching browser tabs.

## 🚀 Features (MVP)

*   **Project Dashboard:** View all projects you own or have access to.
*   **Issue Tracker:**
    *   View open issues in a scrollable list.
    *   Create new issues with titles, descriptions, and labels.
    *   Close issues directly from the app.
*   **Merge Request Viewer:** See status of open MRs (CI/CD status, reviewers).
*   **Secure Authentication:** Uses Personal Access Tokens stored locally/securely.

## 🛠 Tech Stack

*   **Language:** Python 3.10+
*   **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (A modern wrapper around Python's standard Tkinter that supports Dark Mode and rounded corners).
*   **API Wrapper:** [python-gitlab](https://python-gitlab.readthedocs.io/)
*   **Icons:** [Pillow](https://python-pillow.org/) (For rendering images/avatars).

---

## 📂 Project Architecture

We use a **Modular Architecture** to keep the GUI code separate from the GitLab logic. This makes the code easier to maintain.

```text
gitlab-manager-gui/
│
├── assets/                 # Store icons, logo images, fonts
│   └── logo.png
│
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py             # The entry point of the application
│   │
│   ├── api/                # Logic for communicating with GitLab
│   │   ├── __init__.py
│   │   ├── client.py       # Handles authentication & connection
│   │   └── data_fetcher.py # Functions to get projects, issues, etc.
│   │
│   ├── ui/                 # All GUI related code
│   │   ├── __init__.py
│   │   ├── app_window.py   # Main container window
│   │   ├── login_frame.py  # The login screen
│   │   ├── dashboard.py    # The project selection screen
│   │   └── styles.py       # Colors, fonts, and dimensions
│   │
│   └── utils/              # Helper functions
│       ├── __init__.py
│       └── config.py       # Handles saving/loading settings (tokens)
│
├── .env.example            # Example environment variables (if needed)
├── .gitignore              # Files to ignore (e.g., __pycache__, tokens)
├── README.md               # This documentation
└── requirements.txt        # Python dependencies
```

---

## ⚡ Getting Started

### 1. Prerequisites
*   Python installed on your machine.
*   A GitLab Personal Access Token. (Go to **User Settings -> Access Tokens**, create one with `api` scope).

### 2. Installation

Clone the repo and navigate to the folder:

```bash
git clone https://github.com/yourname/gitlab-manager-gui.git
cd gitlab-manager-gui
```

Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install customtkinter python-gitlab pillow
```

### 3. Running the App

```bash
python src/main.py
```

---

## 🗺️ Development Roadmap

### Phase 1: Setup & Authentication
- [ ] Set up the directory structure.
- [ ] Create `src/ui/login_frame.py`: A simple window input for the API Token.
- [ ] Create `src/api/client.py`: Validate the token and connect to GitLab.
- [ ] Save the valid token to a local JSON/Config file so the user doesn't have to log in every time.

### Phase 2: The Dashboard
- [ ] Create `src/ui/dashboard.py`.
- [ ] Fetch the list of projects using `python-gitlab`.
- [ ] Display projects as clickable "Cards" or a List.
- [ ] Clicking a project saves it as the `current_active_project`.

### Phase 3: Issue Management
- [ ] Create a Sidebar menu (Issues, MRs, Settings).
- [ ] Build the "Issue List" view.
- [ ] Add a "Create Issue" button that opens a popup (Toplevel window).
- [ ] Implement the logic to POST the new issue to the API.

### Phase 4: Polish & Packaging
- [ ] Add error handling (e.g., what if the internet cuts out?).
- [ ] Add a refresh button to reload data.
- [ ] Use `pyinstaller` to turn the python script into a real `.exe` or `.app` file.

---

## 📝 Code Starter Examples

Here are snippets to help you start the specific files mentioned in the Architecture.

### 1. `src/api/client.py` (The Backend)
```python
import gitlab

class GitLabClient:
    def __init__(self, token, url='https://gitlab.com'):
        self.gl = gitlab.Gitlab(url, private_token=token)
        self.user = None

    def authenticate(self):
        try:
            self.gl.auth()
            self.user = self.gl.user
            return True, f"Connected as {self.user.username}"
        except Exception as e:
            return False, str(e)
            
    def get_projects(self):
        return self.gl.projects.list(owned=True, per_page=20)
```

### 2. `src/ui/app_window.py` (The GUI Shell)
```python
import customtkinter as ctk
from src.ui.login_frame import LoginFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GitLab Manager")
        self.geometry("800x600")
        
        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Start with Login Screen
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, gl_client):
        print("Login Successful! Switching to Dashboard...")
        self.login_frame.grid_forget()
        # Here you would load: self.dashboard = Dashboard(self, gl_client)
```

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
