import customtkinter as ctk
from src.ui.login_frame import LoginFrame
from src.ui.dashboard import Dashboard
from src.utils.config import load_token, load_app_state, save_app_state, clear_token
from src.api.client import GitLabClient
from src.ui.project_view import ProjectView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GitLab Manager")
        self.geometry("1000x700")
        
        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.gl_client = None
        self.current_frame = None

        # Check for existing token
        saved_token, saved_url = load_token()
        if saved_token:
            self.try_auto_login(saved_token, saved_url)
        else:
            self.show_login()

    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.grid_forget()
            self.current_frame.destroy() # Clean up

        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.switch_frame(LoginFrame, on_login_success=self.on_login_success)

    def try_auto_login(self, token, url):
        # Show a loading screen or just try to connect
        client = GitLabClient(token, url=url)
        success, message = client.authenticate()
        
        if success:
            self.on_login_success(client)
        else:
            # Token might be expired or invalid
            self.show_login()

    def on_login_success(self, gl_client):
        self.gl_client = gl_client
        
        # Check for last active project
        last_project_id = load_app_state("last_project_id")
        if last_project_id:
            print(f"Found last active project ID: {last_project_id}")
            # TODO: In Phase 3, we might jump straight to the project view
            # For now, we go to dashboard to allow selection
            
        self.show_dashboard()

    def show_dashboard(self):
        self.switch_frame(
            Dashboard, 
            gl_client=self.gl_client, 
            on_project_selected=self.on_project_selected,
            on_logout=self.logout,
            on_exit=self.exit_app
        )


    def on_project_selected(self, project):
        print(f"Opening project: {project.name}")
        self.show_project_view(project)

    def show_project_view(self, project):
        self.switch_frame(
            ProjectView,
            gl_client=self.gl_client,
            project=project,
            on_back=self.show_dashboard
        )
        
    def logout(self):
        clear_token()
        self.gl_client = None
        self.show_login()

    def exit_app(self):
        self.destroy()
