import customtkinter as ctk
import threading

class ManageMilestonesDialog(ctk.CTkToplevel):
    def __init__(self, master, fetcher, project_id):
        super().__init__(master)
        self.fetcher = fetcher
        self.project_id = project_id
        
        self.title("Manage Milestones")
        self.geometry("500x600")
        self.transient(master)
        self.after(100, self.grab_set)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create Form
        self.create_frame = ctk.CTkFrame(self)
        self.create_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.create_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.create_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ctk.CTkEntry(self.create_frame, placeholder_text="v1.0")
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(self.create_frame, text="Due Date:").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(self.create_frame, placeholder_text="YYYY-MM-DD (Optional)")
        self.date_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        self.create_btn = ctk.CTkButton(self.create_frame, text="Create Milestone", command=self.create_milestone)
        self.create_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.close_btn = ctk.CTkButton(self.create_frame, text="Close", fg_color="gray", command=self.destroy)
        self.close_btn.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # List
        ctk.CTkLabel(self, text="Existing Milestones", font=("Roboto", 14, "bold")).grid(row=1, column=0, sticky="w", padx=10)
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        threading.Thread(target=self._fetch_and_display, daemon=True).start()

    def _fetch_and_display(self):
        milestones = self.fetcher.fetch_milestones(self.project_id)
        self.after(0, lambda: self._display_milestones(milestones))

    def _display_milestones(self, milestones):
        for i, m in enumerate(milestones):
            frame = ctk.CTkFrame(self.list_frame)
            frame.grid(row=i, column=0, sticky="ew", padx=2, pady=2)
            frame.grid_columnconfigure(0, weight=1)
            
            text = m.title
            if m.due_date: text += f" (Due: {m.due_date})"
            
            lbl = ctk.CTkLabel(frame, text=text)
            lbl.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
            del_btn = ctk.CTkButton(frame, text="Delete", width=60, fg_color="#C42B1C", hover_color="#8E1F14", 
                                  command=lambda m=m: self.delete_milestone(m))
            del_btn.grid(row=0, column=1, padx=5, pady=5)

    def create_milestone(self):
        title = self.title_entry.get()
        due_date = self.date_entry.get()
        if not title: return
        if not due_date: due_date = None
        
        success, msg = self.fetcher.create_milestone(self.project_id, title, due_date)
        if success:
            self.title_entry.delete(0, "end")
            self.date_entry.delete(0, "end")
            self.refresh_list()
        else:
            print(f"Error creating milestone: {msg}")

    def delete_milestone(self, milestone):
        success, msg = self.fetcher.delete_milestone(self.project_id, milestone.id)
        if success:
            self.refresh_list()
        else:
            print(f"Error deleting milestone: {msg}")
