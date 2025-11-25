import customtkinter as ctk
from src.api.client import GitLabClient
from src.utils.config import save_token

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        
        # Center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.title_label = ctk.CTkLabel(self, text="GitLab Manager", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=1, column=0, pady=(20, 10))

        self.subtitle_label = ctk.CTkLabel(self, text="Enter your Personal Access Token", font=("Roboto", 14))
        self.subtitle_label.grid(row=2, column=0, pady=(0, 20))

        self.token_entry = ctk.CTkEntry(self, placeholder_text="glpat-...", width=300, show="*")
        self.token_entry.grid(row=3, column=0, pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, width=300)
        self.login_button.grid(row=4, column=0, pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=5, column=0, pady=5)

    def login(self):
        token = self.token_entry.get()
        if not token:
            self.error_label.configure(text="Please enter a token.")
            return

        self.login_button.configure(state="disabled", text="Connecting...")
        self.update_idletasks()

        client = GitLabClient(token)
        success, message = client.authenticate()

        if success:
            save_token(token)
            self.on_login_success(client)
        else:
            self.error_label.configure(text=message)
            self.login_button.configure(state="normal", text="Login")
