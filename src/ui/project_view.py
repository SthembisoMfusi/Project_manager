import customtkinter as ctk
from src.api.data_fetcher import DataFetcher
from src.ui.issue_list import IssueListFrame
from src.ui.manage_labels_dialog import ManageLabelsDialog
from src.ui.manage_milestones_dialog import ManageMilestonesDialog
from src.ui.manage_boards_dialog import ManageBoardsDialog
from src.ui.manage_templates_dialog import ManageTemplatesDialog

class ProjectView(ctk.CTkFrame):
    def __init__(self, master, gl_client, project, on_back):
        super().__init__(master)
        self.gl_client = gl_client
        self.fetcher = DataFetcher(gl_client)
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

        self.issues_btn = ctk.CTkButton(self.sidebar, text="Issues", command=self.show_issues, width=180, fg_color="transparent", border_width=2, text_color=("gray10", "gray90"))
        self.issues_btn.grid(row=1, column=0, padx=10, pady=10)

        # Management Buttons
        self.lbl_btn = ctk.CTkButton(self.sidebar, text="Manage Labels", command=self.open_labels, width=180, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        self.lbl_btn.grid(row=2, column=0, padx=10, pady=5)

        self.mil_btn = ctk.CTkButton(self.sidebar, text="Manage Milestones", command=self.open_milestones, width=180, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        self.mil_btn.grid(row=3, column=0, padx=10, pady=5)

        self.boards_btn = ctk.CTkButton(self.sidebar, text="Manage Boards", command=self.open_boards, width=180, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        self.boards_btn.grid(row=4, column=0, padx=10, pady=5)

        self.tpl_btn = ctk.CTkButton(self.sidebar, text="Manage Templates", command=self.open_templates, width=180, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        self.tpl_btn.grid(row=5, column=0, padx=10, pady=5)
        
        self.back_btn = ctk.CTkButton(self.sidebar, text="← Back to Dashboard", command=self.on_back, width=180, fg_color="#C42B1C", hover_color="#8E1F14")
        self.back_btn.grid(row=10, column=0, padx=10, pady=20, sticky="s")

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

    def open_labels(self):
        ManageLabelsDialog(self, self.fetcher, self.project.id)

    def open_milestones(self):
        ManageMilestonesDialog(self, self.fetcher, self.project.id)

    def open_boards(self):
        ManageBoardsDialog(self, self.fetcher, self.project.id)

    def open_templates(self):
        ManageTemplatesDialog(self)
