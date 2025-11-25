import customtkinter as ctk
from src.api.data_fetcher import DataFetcher
from src.utils.config import save_app_state

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, gl_client, on_project_selected, on_logout, on_exit):
        super().__init__(master)
        self.gl_client = gl_client
        self.on_project_selected = on_project_selected
        self.on_logout = on_logout
        self.on_exit = on_exit
        self.fetcher = DataFetcher(gl_client)

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Project list area

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1) # Spacer

        self.title_label = ctk.CTkLabel(self.header_frame, text=f"Welcome, {gl_client.user.username}", font=("Roboto", 18, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=15)

        # Buttons
        self.refresh_button = ctk.CTkButton(self.header_frame, text="Refresh", command=self.load_projects, width=100)
        self.refresh_button.grid(row=0, column=2, padx=(0, 10), pady=15)

        self.logout_button = ctk.CTkButton(self.header_frame, text="Logout", command=self.on_logout, width=100, fg_color="#555555", hover_color="#333333")
        self.logout_button.grid(row=0, column=3, padx=(0, 10), pady=15)

        self.exit_button = ctk.CTkButton(self.header_frame, text="Exit", command=self.on_exit, width=80, fg_color="#C42B1C", hover_color="#8E1F14")
        self.exit_button.grid(row=0, column=4, padx=(0, 20), pady=15)

        # --- Project List ---
        self.project_list_frame = ctk.CTkScrollableFrame(self, label_text="Your Projects")
        self.project_list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.project_list_frame.grid_columnconfigure(0, weight=1)

        self.load_projects()

    def load_projects(self):
        projects = self.fetcher.fetch_projects()
        
        if not projects:
            no_projects_label = ctk.CTkLabel(self.project_list_frame, text="No projects found.")
            no_projects_label.grid(row=0, column=0, pady=20)
            return

        for i, project in enumerate(projects):
            self.create_project_card(project, i)

    def create_project_card(self, project, index):
        card = ctk.CTkFrame(self.project_list_frame)
        card.grid(row=index, column=0, sticky="ew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        # Project Name
        name_label = ctk.CTkLabel(card, text=project.name_with_namespace, font=("Roboto", 14, "bold"), anchor="w")
        name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # Project Description (truncated)
        description = project.description if project.description else "No description"
        if len(description) > 80:
            description = description[:77] + "..."
            
        desc_label = ctk.CTkLabel(card, text=description, font=("Roboto", 12), text_color="gray", anchor="w")
        desc_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # Select Button
        select_btn = ctk.CTkButton(card, text="Select", width=80, command=lambda p=project: self.select_project(p))
        select_btn.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    def select_project(self, project):
        print(f"Selected project: {project.name} (ID: {project.id})")
        save_app_state("last_project_id", project.id)
        self.on_project_selected(project)
