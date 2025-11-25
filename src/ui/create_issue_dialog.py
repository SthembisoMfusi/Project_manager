import customtkinter as ctk

class CreateIssueDialog(ctk.CTkToplevel):
    def __init__(self, master, on_create):
        super().__init__(master)
        self.on_create = on_create
        
        self.title("Create New Issue")
        self.geometry("500x400")
        
        # Make it modal
        self.transient(master)
        self.after(100, self.grab_set) # Wait for window to be created
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title Input
        self.title_label = ctk.CTkLabel(self, text="Title", font=("Roboto", 14, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Issue Title")
        self.title_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Description Input
        self.desc_label = ctk.CTkLabel(self, text="Description", font=("Roboto", 14, "bold"))
        self.desc_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="nw")
        
        self.desc_textbox = ctk.CTkTextbox(self, height=150)
        self.desc_textbox.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", fg_color="gray", command=self.destroy)
        self.cancel_button.grid(row=0, column=1, padx=10)

        self.create_button = ctk.CTkButton(self.button_frame, text="Create Issue", command=self.create_issue)
        self.create_button.grid(row=0, column=2, padx=10)

    def create_issue(self):
        title = self.title_entry.get()
        description = self.desc_textbox.get("1.0", "end-1c")
        
        if not title:
            # Simple validation
            self.title_entry.configure(placeholder_text="Title is required!", placeholder_text_color="red")
            return

        self.create_button.configure(state="disabled", text="Creating...")
        self.on_create(title, description, self)
