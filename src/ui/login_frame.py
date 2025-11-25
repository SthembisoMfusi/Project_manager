import customtkinter as ctk
import webbrowser
from src.api.client import GitLabClient
from src.utils.config import save_token

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        
        # Center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)

        self.title_label = ctk.CTkLabel(self, text="GitLab Manager", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=1, column=0, pady=(20, 10))

        self.subtitle_label = ctk.CTkLabel(self, text="Enter your Personal Access Token", font=("Roboto", 14))
        self.subtitle_label.grid(row=2, column=0, pady=(0, 5))

        # Help Link
        self.help_label = ctk.CTkLabel(self, text="Where do I get my token?", font=("Roboto", 12, "underline"), text_color=("#3B8ED0", "#1F6AA5"), cursor="hand2")
        self.help_label.grid(row=3, column=0, pady=(0, 20))
        self.help_label.bind("<Button-1>", lambda e: self.open_help_link())

        # URL Entry
        self.url_label = ctk.CTkLabel(self, text="GitLab URL (Optional)", font=("Roboto", 12))
        self.url_label.grid(row=4, column=0, pady=(5, 0))
        
        self.url_entry = ctk.CTkEntry(self, placeholder_text="https://gitlab.wethinkco.de", width=300)
        self.url_entry.grid(row=5, column=0, pady=(0, 10))
        self.url_entry.insert(0, "https://gitlab.wethinkco.de")

        # Token Entry
        self.token_entry = ctk.CTkEntry(self, placeholder_text="glpat-...", width=300, show="*")
        self.token_entry.grid(row=6, column=0, pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, width=300)
        self.login_button.grid(row=7, column=0, pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=8, column=0, pady=5)

    def open_help_link(self):
        url = self.url_entry.get().strip()
        if not url:
            url = "https://gitlab.wethinkco.de"
        
        # Ensure URL has protocol
        if not url.startswith("http"):
            url = "https://" + url
            
        # Remove trailing slash
        url = url.rstrip("/")
        
        if "gitlab.wethinkco.de" in url:
            full_url = f"{url}/-/user_settings/personal_access_tokens?page=1&state=active&sort=expires_asc"
        else:
            full_url = f"{url}/-/profile/personal_access_tokens"
            
        webbrowser.open(full_url)

    def login(self):
        token = self.token_entry.get()
        url = self.url_entry.get().strip()
        
        if not token:
            self.error_label.configure(text="Please enter a token.")
            return

        if not url:
            url = "https://gitlab.wethinkco.de"
            
        # Ensure URL has protocol
        if not url.startswith("http"):
            url = "https://" + url

        self.login_button.configure(state="disabled", text="Connecting...")
        self.update_idletasks()

        client = GitLabClient(token, url=url)
        success, message = client.authenticate()

        if success:
            save_token(token, url)
            self.on_login_success(client)
        else:
            self.error_label.configure(text=message)
            self.login_button.configure(state="normal", text="Login")
