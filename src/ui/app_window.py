import customtkinter as ctk
from src.ui.login_frame import LoginFrame
from src.utils.config import load_token
from src.api.client import GitLabClient

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GitLab Manager")
        self.geometry("900x600")
        
        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.gl_client = None

        # Check for existing token
        saved_token = load_token()
        if saved_token:
            self.try_auto_login(saved_token)
        else:
            self.show_login()

    def show_login(self):
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def try_auto_login(self, token):
        # Show a loading screen or just try to connect
        # For now, we'll just try to connect synchronously (could be improved with a splash screen)
        client = GitLabClient(token)
        success, message = client.authenticate()
        
        if success:
            self.on_login_success(client)
        else:
            # Token might be expired or invalid
            self.show_login()

    def on_login_success(self, gl_client):
        self.gl_client = gl_client
        if hasattr(self, 'login_frame'):
            self.login_frame.grid_forget()
        
        self.show_dashboard()

    def show_dashboard(self):
        # Placeholder for Dashboard
        self.dashboard_label = ctk.CTkLabel(self, text=f"Welcome, {self.gl_client.user.username}!\nDashboard coming soon...", font=("Roboto", 20))
        self.dashboard_label.grid(row=0, column=0, sticky="nsew")
