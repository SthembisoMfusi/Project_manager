import customtkinter as ctk
import threading
from src.api.data_fetcher import DataFetcher
from src.ui.create_issue_dialog import CreateIssueDialog

class IssueListFrame(ctk.CTkFrame):
    def __init__(self, master, gl_client, project):
        super().__init__(master)
        self.gl_client = gl_client
        self.project = project
        self.fetcher = DataFetcher(gl_client)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Open Issues", font=("Roboto", 18, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.create_btn = ctk.CTkButton(self.header_frame, text="+ New Issue", width=100, command=self.open_create_dialog)
        self.create_btn.grid(row=0, column=1)

        # --- List Area ---
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.list_frame.grid_columnconfigure(0, weight=1)

        # --- Loading Indicator ---
        self.loading_label = ctk.CTkLabel(self, text="Loading issues...", font=("Roboto", 14))
        self.loading_label.grid(row=1, column=0)
        
        # Start fetching
        self.refresh_issues()

    def refresh_issues(self):
        # Clear list
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        # Show loading
        self.loading_label.lift()
        self.list_frame.grid_remove() # Hide list while loading
        
        # Fetch in background
        threading.Thread(target=self._fetch_issues_thread, daemon=True).start()

    def _fetch_issues_thread(self):
        issues = self.fetcher.fetch_issues(self.project.id)
        # Update UI on main thread (ctk is generally thread-safe for simple updates, but best practice is after)
        self.after(0, lambda: self._update_ui(issues))

    def _update_ui(self, issues):
        self.loading_label.lower() # Hide loading
        self.list_frame.grid() # Show list
        
        if not issues:
            lbl = ctk.CTkLabel(self.list_frame, text="No open issues found.")
            lbl.grid(row=0, column=0, pady=20)
            return

        for i, issue in enumerate(issues):
            self.create_issue_card(issue, i)

    def create_issue_card(self, issue, index):
        card = ctk.CTkFrame(self.list_frame)
        card.grid(row=index, column=0, sticky="ew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ctk.CTkLabel(card, text=f"#{issue.iid} {issue.title}", font=("Roboto", 14, "bold"), anchor="w")
        title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Meta
        meta_text = f"Created by {issue.author['username']} • {issue.updated_at[:10]}"
        meta_label = ctk.CTkLabel(card, text=meta_text, font=("Roboto", 12), text_color="gray", anchor="w")
        meta_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

    def open_create_dialog(self):
        CreateIssueDialog(self, self.on_issue_created)

    def on_issue_created(self, title, description, dialog):
        success, result = self.fetcher.create_issue(self.project.id, title, description)
        dialog.destroy()
        
        if success:
            print(f"Created issue: {result.title}")
            self.refresh_issues()
        else:
            print(f"Failed to create issue: {result}")
            # Ideally show an error dialog here
