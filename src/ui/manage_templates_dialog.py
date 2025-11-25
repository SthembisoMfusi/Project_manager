import customtkinter as ctk
from src.utils.template_manager import TemplateManager

class ManageTemplatesDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.manager = TemplateManager()
        
        self.title("Manage Templates")
        self.geometry("600x500")
        self.transient(master)
        self.after(100, self.grab_set)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # List (Left) and Edit (Right) - simplified to just list with edit/delete
      
        self.grid_columnconfigure(0, weight=1) # List
        self.grid_columnconfigure(1, weight=2) # Editor
        
        # --- Left: List ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Templates")
        self.list_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        # --- Right: Editor ---
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.editor_frame.grid_columnconfigure(1, weight=1)
        self.editor_frame.grid_rowconfigure(3, weight=1)
        
        ctk.CTkLabel(self.editor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(self.editor_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(self.editor_frame, text="Title Prefix:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ctk.CTkEntry(self.editor_frame)
        self.title_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(self.editor_frame, text="Content:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.content_text = ctk.CTkTextbox(self.editor_frame)
        self.content_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        
        self.close_btn = ctk.CTkButton(self.btn_frame, text="Close", fg_color="gray", command=self.destroy, width=80)
        self.close_btn.pack(side="right", padx=5)

        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save", command=self.save_template, width=80)
        self.save_btn.pack(side="right", padx=5)
        
        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete", fg_color="#C42B1C", hover_color="#8E1F14", command=self.delete_template, width=80)
        self.delete_btn.pack(side="right", padx=5)
        
        self.new_btn = ctk.CTkButton(self.btn_frame, text="New", command=self.clear_editor, width=80)
        self.new_btn.pack(side="left", padx=5)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        names = self.manager.get_template_names()
        for name in names:
            btn = ctk.CTkButton(self.list_frame, text=name, fg_color="transparent", border_width=1, 
                              text_color=("gray10", "gray90"), anchor="w",
                              command=lambda n=name: self.load_template(n))
            btn.pack(fill="x", pady=2)

    def load_template(self, name):
        tmpl = self.manager.get_template(name)
        if tmpl:
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, name)
            self.name_entry.configure(state="disabled") # Cannot rename key easily
            
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, tmpl['title'])
            
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", tmpl['description'])

    def clear_editor(self):
        self.name_entry.configure(state="normal")
        self.name_entry.delete(0, "end")
        self.title_entry.delete(0, "end")
        self.content_text.delete("1.0", "end")

    def save_template(self):
        name = self.name_entry.get()
        title = self.title_entry.get()
        desc = self.content_text.get("1.0", "end-1c")
        
        if name:
            self.manager.save_template(name, title, desc)
            self.refresh_list()
            self.name_entry.configure(state="disabled")

    def delete_template(self):
        name = self.name_entry.get()
        if name:
            self.manager.delete_template(name)
            self.refresh_list()
            self.clear_editor()
