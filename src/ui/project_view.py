import customtkinter as ctk
from src.ui.issue_list import IssueListFrame

class ProjectView(ctk.CTkFrame):
    def __init__(self, master, gl_client, project, on_back):
        super().__init__(master)
        self.gl_client = gl_client
        self.project = project
        self.on_back = on_back

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.project_label = ctk.CTkLabel(self.sidebar, text=project.name, font=("Roboto", 16, "bold"), wraplength=180)
        self.project_label.grid(row=0, column=0, padx=20, pady=20)

        self.issues_btn = ctk.CTkButton(self.sidebar, text="Issues", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.issues_btn.grid(row=1, column=0, padx=20, pady=10)

        self.back_btn = ctk.CTkButton(self.sidebar, text="← Back to Dashboard", command=self.on_back, fg_color="transparent", text_color="gray")
        self.back_btn.grid(row=5, column=0, padx=20, pady=20)

        # --- Content Area ---
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Load Issue List by default
        self.show_issues()

    def show_issues(self):
        self.issue_list = IssueListFrame(self.content_area, self.gl_client, self.project)
        self.issue_list.grid(row=0, column=0, sticky="nsew")
