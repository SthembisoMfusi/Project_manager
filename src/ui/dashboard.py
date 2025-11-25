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
        
        self.current_page = 1
        self.per_page = 10
        self.search_query = ""

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Project list area

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1) # Spacer

        self.title_label = ctk.CTkLabel(self.header_frame, text=f"Welcome, {gl_client.user.username}", font=("Roboto", 18, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=15)

        # Buttons
        self.logout_button = ctk.CTkButton(self.header_frame, text="Logout", command=self.on_logout, width=100, fg_color="#555555", hover_color="#333333")
        self.logout_button.grid(row=0, column=3, padx=(0, 10), pady=15)

        self.exit_button = ctk.CTkButton(self.header_frame, text="Exit", command=self.on_exit, width=80, fg_color="#C42B1C", hover_color="#8E1F14")
        self.exit_button.grid(row=0, column=4, padx=(0, 20), pady=15)

        # --- Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(20, 0))
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search projects...")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
        
        self.search_btn = ctk.CTkButton(self.search_frame, text="Search", width=80, command=self.perform_search)
        self.search_btn.grid(row=0, column=1)

        # --- Project List ---
        self.project_list_frame = ctk.CTkScrollableFrame(self, label_text="Your Projects")
        self.project_list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.project_list_frame.grid_columnconfigure(0, weight=1)

        # --- Pagination ---
        self.pagination_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pagination_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.pagination_frame.grid_columnconfigure(1, weight=1)
        
        self.prev_btn = ctk.CTkButton(self.pagination_frame, text="Previous", width=80, command=self.prev_page, state="disabled")
        self.prev_btn.grid(row=0, column=0)
        
        self.page_label = ctk.CTkLabel(self.pagination_frame, text=f"Page {self.current_page}")
        self.page_label.grid(row=0, column=1)
        
        self.next_btn = ctk.CTkButton(self.pagination_frame, text="Next", width=80, command=self.next_page)
        self.next_btn.grid(row=0, column=2)

        self.load_projects()

    def perform_search(self):
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1
        self.load_projects()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_projects()

    def next_page(self):
        self.current_page += 1
        self.load_projects()

    def load_projects(self):
        # Clear list
        for widget in self.project_list_frame.winfo_children():
            widget.destroy()
            
        projects = self.fetcher.fetch_projects(search=self.search_query, page=self.current_page, per_page=self.per_page)
        
        # Update Pagination UI
        self.page_label.configure(text=f"Page {self.current_page}")
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        
        # If fewer projects than per_page, disable next (simple heuristic)
        self.next_btn.configure(state="normal" if len(projects) == self.per_page else "disabled")

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
