import customtkinter as ctk
import threading
from src.utils.template_manager import TemplateManager

class CreateIssueDialog(ctk.CTkToplevel):
    def __init__(self, master, fetcher, project_id, on_save, issue=None):
        super().__init__(master)
        self.fetcher = fetcher
        self.project_id = project_id
        self.on_save = on_save
        self.issue = issue 
        self.template_manager = TemplateManager()
        
        title_text = "Edit Issue" if issue else "New Issue"
        self.title(title_text)
        self.geometry("900x650") # Slightly taller for templates
        
        # Make it modal
        self.transient(master)
        self.after(100, self.grab_set)
        
        self.grid_columnconfigure(0, weight=3) # Main content
        self.grid_columnconfigure(1, weight=1) # Sidebar
        self.grid_rowconfigure(1, weight=1)

        # --- Header: Templates (Only for New Issue) ---
        if not issue:
            self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 0))
            
            ctk.CTkLabel(self.header_frame, text="Load Template:").pack(side="left", padx=(0, 10))
            
            self.template_var = ctk.StringVar(value="Select Template")
            self.template_menu = ctk.CTkOptionMenu(self.header_frame, variable=self.template_var, command=self.load_template)
            self.template_menu.pack(side="left")
            self.refresh_template_menu()

        # --- Left Column: Content ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(3, weight=1)

        # Title
        ctk.CTkLabel(self.content_frame, text="Title (required)", font=("Roboto", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.title_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Issue Title")
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        if issue: self.title_entry.insert(0, issue.title)

        # Description
        ctk.CTkLabel(self.content_frame, text="Description", font=("Roboto", 14, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.desc_textbox = ctk.CTkTextbox(self.content_frame)
        self.desc_textbox.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
        if issue and issue.description: self.desc_textbox.insert("1.0", issue.description)

        # --- Right Column: Metadata ---
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray20"))
        self.sidebar_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # Assignee
        ctk.CTkLabel(self.sidebar_frame, text="Assignee", font=("Roboto", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        self.assignee_var = ctk.StringVar(value="Unassigned")
        self.assignee_menu = ctk.CTkOptionMenu(self.sidebar_frame, variable=self.assignee_var, values=["Unassigned"])
        self.assignee_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        self.assignee_map = {} # Name -> ID

        # Labels
        ctk.CTkLabel(self.sidebar_frame, text="Labels", font=("Roboto", 14, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))
        self.labels_frame = ctk.CTkScrollableFrame(self.sidebar_frame, height=150)
        self.labels_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 15))
        self.label_vars = {} # Label Name -> BooleanVar

        # Milestone
        ctk.CTkLabel(self.sidebar_frame, text="Milestone", font=("Roboto", 14, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=(0, 5))
        self.milestone_var = ctk.StringVar(value="No Milestone")
        self.milestone_menu = ctk.CTkOptionMenu(self.sidebar_frame, variable=self.milestone_var, values=["No Milestone"])
        self.milestone_menu.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 15))
        self.milestone_map = {} # Title -> ID

        # --- Bottom: Buttons ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        self.button_frame.grid_columnconfigure(0, weight=1)

        # Save Template Button (Left aligned)
        if not issue:
            self.save_tmpl_btn = ctk.CTkButton(self.button_frame, text="Save as Template", fg_color="#555555", command=self.save_as_template)
            self.save_tmpl_btn.grid(row=0, column=0, sticky="w")

        # Action Buttons (Right aligned)
        ctk.CTkButton(self.button_frame, text="Cancel", fg_color="gray", command=self.destroy).grid(row=0, column=1, padx=10, sticky="e")
        self.save_btn = ctk.CTkButton(self.button_frame, text="Save Changes" if issue else "Create Issue", command=self.save)
        self.save_btn.grid(row=0, column=2, padx=10, sticky="e")
        
        # Spacer to push action buttons right
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=0)


        # Load metadata in background
        threading.Thread(target=self.load_metadata, daemon=True).start()

    def load_metadata(self):
        members = self.fetcher.fetch_members(self.project_id)
        labels = self.fetcher.fetch_labels(self.project_id)
        milestones = self.fetcher.fetch_milestones(self.project_id)
        
        self.after(0, lambda: self.populate_metadata(members, labels, milestones))

    def populate_metadata(self, members, labels, milestones):
        # Assignees
        assignee_values = ["Unassigned"]
        for m in members:
            name = m.username
            self.assignee_map[name] = m.id
            assignee_values.append(name)
        self.assignee_menu.configure(values=assignee_values)
        
        # Pre-select assignee if editing
        if self.issue and self.issue.assignee:
            self.assignee_var.set(self.issue.assignee['username'])

        # Labels
        current_labels = self.issue.labels if self.issue else []
        for l in labels:
            var = ctk.BooleanVar(value=l.name in current_labels)
            self.label_vars[l.name] = var
            chk = ctk.CTkCheckBox(self.labels_frame, text=l.name, variable=var)
            chk.pack(anchor="w", pady=2)

        # Milestones
        milestone_values = ["No Milestone"]
        for m in milestones:
            self.milestone_map[m.title] = m.id
            milestone_values.append(m.title)
        self.milestone_menu.configure(values=milestone_values)

        # Pre-select milestone if editing
        if self.issue and self.issue.milestone:
            self.milestone_var.set(self.issue.milestone['title'])

    def refresh_template_menu(self):
        templates = self.template_manager.get_template_names()
        if templates:
            self.template_menu.configure(values=templates)
        else:
            self.template_menu.configure(values=["No Templates"])

    def load_template(self, template_name):
        if template_name == "No Templates": return
        
        tmpl = self.template_manager.get_template(template_name)
        if tmpl:
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, tmpl['title'])
            
            self.desc_textbox.delete("1.0", "end")
            self.desc_textbox.insert("1.0", tmpl['description'])

    def save_as_template(self):
        title = self.title_entry.get()
        description = self.desc_textbox.get("1.0", "end-1c")
        
        if not title:
            return # Should probably show error

        # Ask for template name
        dialog = ctk.CTkInputDialog(text="Enter template name:", title="Save Template")
        name = dialog.get_input()
        
        if name:
            self.template_manager.save_template(name, title, description)
            self.refresh_template_menu()

    def save(self):
        title = self.title_entry.get()
        description = self.desc_textbox.get("1.0", "end-1c")
        
        if not title:
            self.title_entry.configure(placeholder_text="Title is required!", placeholder_text_color="red")
            return

        # Collect metadata
        assignee_name = self.assignee_var.get()
        assignee_id = self.assignee_map.get(assignee_name)
        
        selected_labels = [name for name, var in self.label_vars.items() if var.get()]
        
        milestone_title = self.milestone_var.get()
        milestone_id = self.milestone_map.get(milestone_title)

        self.save_btn.configure(state="disabled", text="Saving...")
        
        self.on_save(
            title=title, 
            description=description, 
            assignee_id=assignee_id, 
            labels=selected_labels, 
            milestone_id=milestone_id,
            dialog=self
        )
